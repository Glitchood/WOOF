<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { authStore, api, type Transaction } from '$lib';

  let user: { userId: number; username: string; token: string } | null = null;
  let balance = 0;
  let transactions: Transaction[] = [];
  let loading = false;
  let error: string | null = null;


  let toUsername = '';
  let amount = 0;
  let description = '';

  onMount(async () => {
    authStore.init();
    authStore.subscribe(value => {
      user = value;
      if (!value) {
        goto('/');
      }
    });

    if (user) {
      await loadData();
    }
  });

  async function loadData() {
    if (!user) return;
    
    loading = true;
    error = null;
    console.log("loading data...");
    try {
      const account = await api.getMe(user.token);
      balance = account.balance;
      transactions = await api.getTransactions(user.userId);
    } catch (e) {
      console.log("ERROR")
      error = e instanceof Error ? e.message : 'Failed to load data';
    } finally {
      loading = false;
    }
    console.log("finished loading data");
  }

  async function handleTransfer() {
    if (!user) return;

    loading = true;
    error = null;
    try {
      await api.transferFunds({
        to_user_name: toUsername,
        amount: amount,
        description: description
      });
      toUserId = 0;
      amount = 0;
      description = '';
      await loadData();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Transfer failed';
    } finally {
      loading = false;
    }
  }

  function handleLogout() {
    authStore.logout();
    goto('/');
  }
</script>

<div class="container">
  <header>
    <h1>Banking Dashboard</h1>
    <button on:click={handleLogout}>Logout</button>
  </header>

  <!--{#if error}
    <div class="error">{error}</div>
  {/if}-->

  {#if user}
    <div class="balance-card">
      <h2>Welcome, {user.username}!</h2>
      <p class="balance">${balance.toFixed(2)}</p>
      <p class="label">Current Balance</p>
    </div>

    <div class="transfer-card">
      <h3>Transfer Funds</h3>
      <form on:submit|preventDefault={handleTransfer}>
        
        <input
          type="text"
          placeholder="Recipient Username"
          bind:value={toUsername}
          required
        />
        <input
          type="number"
          placeholder="Amount"
          bind:value={amount}
          step="0.01"
          required
        />
        <input
          type="text"
          placeholder="Description"
          bind:value={description}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Transfer'}
        </button>
      </form>
    </div>

  {/if}
</div>

<style>
  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  h1 {
    color: #333;
  }

  button {
    background: #667eea;
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
  }

  button:hover {
    background: #5568d3;
  }

  button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .balance-card, .transfer-card, .transactions-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
  }

  .balance {
    font-size: 3rem;
    font-weight: bold;
    color: #667eea;
    margin: 0.5rem 0;
  }
  
  .userid {
    font-size: 0.9rem;
    color: #333;
  }

  .label {
    color: #666;
    text-transform: uppercase;
    font-size: 0.9rem;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }

  input {
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
  }

  .transactions-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 1rem;
  }

  .transaction {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
    border-left: 4px solid #c62828;
  }

  .transaction.positive {
    border-left-color: #4caf50;
  }

  .transaction .amount {
    font-weight: bold;
    font-size: 1.2rem;
  }

  .transaction.positive .amount {
    color: #4caf50;
  }

  .transaction:not(.positive) .amount {
    color: #c62828;
  }

  .id {
    font-size: 0.85rem;
    color: #999;
    margin-left: 0.5rem;
  }

  .error {
    background: #ffebee;
    color: #c62828;
    padding: 1rem;
    border-radius: 6px;
    margin-bottom: 1rem;
  }
</style>
