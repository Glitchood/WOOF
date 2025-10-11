<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/auth';
	import { api, type Transaction } from '$lib/api';

	let loading = $state(true);
	let transactions: Transaction[] = $state([]);
	let showModal = $state(false);
	let toUsername = $state('');
	let amount = $state('');
	let description = $state('');
	let error = $state('');

	onMount(async () => {
		if (!$authStore.token) {
			goto('/');
			return;
		}
		await loadData();
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

		<div class="transactions">
			<h2>Recent Transactions</h2>
			{#if transactions.length === 0}
				<p class="empty">No transactions yet</p>
			{:else}
				{#each transactions as tx}
					<div class="tx-item">
						<div>
							<div class="tx-desc">{tx.description}</div>
							<div class="tx-meta">
								{tx.from_user_id === $authStore.user?.id ? `To: ${tx.to_user_id}` : `From: ${tx.from_user_id}`}
							</div>
						</div>
						<div class="tx-amount" class:negative={tx.from_user_id === $authStore.user?.id}>
							{tx.from_user_id === $authStore.user?.id ? '-' : '+'}${tx.amount.toFixed(2)}
						</div>
					</div>
				{/each}
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
	.dashboard { max-width: 1000px; margin: 0 auto; padding: 2rem; }
	.loading { text-align: center; padding: 3rem; }
	.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
	.btn { padding: 0.75rem 1.5rem; background: #2563eb; color: white; border-radius: 0.5rem; font-weight: 600; }
	.btn:hover { background: #1d4ed8; }
	.btn-secondary { padding: 0.75rem 1.5rem; background: #f1f5f9; color: #0f172a; border-radius: 0.5rem; }
	.balance-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 1rem; padding: 2rem; color: white; margin-bottom: 2rem; }
	.label { font-size: 0.875rem; opacity: 0.9; text-transform: uppercase; }
	.amount { font-size: 3rem; font-weight: 700; margin-top: 0.5rem; }
	.transactions { background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
	.empty { text-align: center; padding: 2rem; color: #64748b; }
	.tx-item { display: flex; justify-content: space-between; padding: 1rem; background: #f8fafc; border-radius: 0.5rem; margin-bottom: 0.75rem; }
	.tx-desc { font-weight: 500; }
	.tx-meta { font-size: 0.875rem; color: #94a3b8; margin-top: 0.25rem; }
	.tx-amount { font-size: 1.25rem; font-weight: 700; color: #10b981; }
	.tx-amount.negative { color: #ef4444; }
	.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
	.modal { background: white; border-radius: 1rem; padding: 2rem; width: 90%; max-width: 500px; }
	.alert { padding: 0.875rem; background: #fee2e2; color: #991b1b; border-radius: 0.5rem; margin-bottom: 1rem; }
	form { display: flex; flex-direction: column; gap: 1.5rem; }
	label { display: flex; flex-direction: column; gap: 0.5rem; font-weight: 500; }
	input { padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 0.5rem; }
	input:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
	.actions { display: flex; gap: 1rem; justify-content: flex-end; }
</style>
