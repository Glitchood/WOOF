<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/auth';
	import { api, type Transaction } from '$lib/api';

	let loading = $state(true);
	let transactions: Transaction[] = $state([]);
	let showModal = $state(false);
	let toUsername = $state('');
	let amount = $state('');
	let description = $state('');
	let error = $state('');

	onMount(() => {
		loadData();
	});

	async function loadData() {
		try {
			loading = true;
			const user = await api.getMe();
			authStore.updateUser(user);
			if (user.id) {
				transactions = await api.getTransactions(user.id);
			}
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	}

	async function handleTransfer(e: Event) {
		e.preventDefault();
		error = '';
		try {
			await api.createTransaction({
      to_user_name: toUsername,
      amount: parseFloat(amount),
      description
      });
			showModal = false;
			toUsername = '';
			amount = '';
			description = '';
			await loadData();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Transfer failed';
		}
	}
</script>

<div class="dashboard">
	{#if loading}
		<div class="loading">Loading...</div>
	{:else}
		<div class="header">
			<h1>Dashboard</h1>
			<button class="btn" onclick={() => (showModal = true)}>💸 Send Money</button>
		</div>

		<div class="balance-card">
			<div class="label">Available Balance</div>
			<div class="amount">${($authStore.user?.balance || 0).toFixed(2)}</div>
		</div>

		<div class="transactions-card">
			<h2>Transaction History</h2>
			{#if transactions.length === 0}
				<p class="empty">No transactions yet</p>
			{:else}
				<div class="transactions-list">
					{#each transactions as tx}
						<div class="transaction" class:positive={tx.to_user_id === $authStore.user?.id}>
							<div class="tx-info">
								<div class="tx-desc">{tx.description}</div>
								<div class="tx-date">{new Date(tx.timestamp).toLocaleString()}</div>
							</div>
							<div class="tx-amount" class:positive={tx.to_user_id === $authStore.user?.id}>
								{tx.to_user_id === $authStore.user?.id ? '+' : '-'}${tx.amount.toFixed(2)}
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	{/if}
</div>

{#if showModal}
	<div class="modal-overlay" onclick={() => (showModal = false)}>
		<div class="modal" onclick={(e) => e.stopPropagation()}>
			<h3>Send Money</h3>
			{#if error}
				<div class="alert">{error}</div>
			{/if}
			<form onsubmit={handleTransfer}>
				<label>Recipient Username
					<input type="text" bind:value={toUsername} required />
				</label>
				<label>Amount
					<input type="number" step="0.01" bind:value={amount} required />
				</label>
				<label>Description
					<input type="text" bind:value={description} required />
				</label>
				<div class="actions">
					<button type="button" class="btn-secondary" onclick={() => (showModal = false)}>Cancel</button>
					<button type="submit" class="btn">Send</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<style>
	.dashboard {
		max-width: 900px;
		margin: 0 auto;
		padding: 2rem;
	}

	.loading {
		text-align: center;
		padding: 3rem;
		color: var(--text-secondary);
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
	}

	h1 {
		color: var(--text-primary);
		margin: 0;
	}

	.btn {
		background: linear-gradient(135deg, var(--primary), var(--accent));
		color: white;
		padding: 0.75rem 1.5rem;
		border: none;
		border-radius: 8px;
		cursor: pointer;
		font-weight: 500;
		transition: transform 0.2s;
	}

	.btn:hover {
		transform: translateY(-2px);
	}

	.balance-card, .transactions-card {
		background: var(--bg-primary);
		padding: 2rem;
		border-radius: 12px;
		box-shadow: var(--shadow-lg);
		margin-bottom: 2rem;
	}

	.balance-card {
		background: linear-gradient(135deg, var(--primary), var(--accent));
		color: white;
		text-align: center;
	}

	.label {
		font-size: 0.9rem;
		opacity: 0.9;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: 0.5rem;
	}

	.amount {
		font-size: 3rem;
		font-weight: bold;
		margin: 0.5rem 0;
	}

	.transactions-card h2 {
		margin-top: 0;
		color: var(--text-primary);
	}

	.empty {
		text-align: center;
		color: var(--text-secondary);
		padding: 2rem;
	}

	.transactions-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.transaction {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		background: var(--bg-secondary);
		border-radius: 8px;
		border-left: 4px solid var(--error);
	}

	.transaction.positive {
		border-left-color: var(--success);
	}

	.tx-info {
		flex: 1;
	}

	.tx-desc {
		font-weight: 500;
		color: var(--text-primary);
		margin-bottom: 0.25rem;
	}

	.tx-date {
		font-size: 0.85rem;
		color: var(--text-secondary);
	}

	.tx-amount {
		font-size: 1.25rem;
		font-weight: bold;
		color: var(--error);
	}

	.tx-amount.positive {
		color: var(--success);
	}

	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}

	.modal {
		background: var(--bg-primary);
		padding: 2rem;
		border-radius: 12px;
		box-shadow: var(--shadow-xl);
		min-width: 400px;
		max-width: 90%;
	}

	.modal h3 {
		margin-top: 0;
		color: var(--text-primary);
	}

	.alert {
		background: var(--error-bg);
		color: var(--error);
		padding: 0.75rem;
		border-radius: 6px;
		margin-bottom: 1rem;
		font-size: 0.9rem;
	}

	form {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	label {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		color: var(--text-primary);
		font-weight: 500;
	}

	input {
		padding: 0.75rem;
		border: 1px solid var(--border);
		border-radius: 6px;
		font-size: 1rem;
		background: var(--bg-primary);
		color: var(--text-primary);
	}

	input:focus {
		outline: none;
		border-color: var(--primary);
	}

	.actions {
		display: flex;
		gap: 1rem;
		margin-top: 0.5rem;
	}

	.btn-secondary {
		flex: 1;
		padding: 0.75rem;
		border: 1px solid var(--border);
		background: var(--bg-secondary);
		color: var(--text-primary);
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
	}

	.btn-secondary:hover {
		background: var(--bg-tertiary);
	}

	button[type="submit"] {
		flex: 1;
	}
</style>
