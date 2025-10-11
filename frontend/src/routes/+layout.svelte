<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { authStore } from '$lib/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { api } from '$lib/api';

	let { children } = $props();

	onMount(async () => {
		const auth = $authStore;
		if (auth.token && !auth.user) {
			try {
				const user = await api.getMe();
				authStore.updateUser(user);
			} catch (error) {
				authStore.logout();
				goto('/');
			}
		}
	});

	function handleLogout() {
		authStore.logout();
		goto('/');
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if $authStore.user}
	<nav class="navbar">
		<div class="container">
			<div class="nav-brand">
				<h2>🏦 WOOF Bank</h2>
			</div>
			<div class="nav-items">
				<span class="user-info">
					Welcome, <strong>{$authStore.user.username}</strong>
				</span>
				<button class="btn btn-secondary" onclick={handleLogout}>Logout</button>
			</div>
		</div>
	</nav>
{/if}

<main>
	{@render children?.()}
</main>

<style>
	.navbar {
		background-color: var(--bg-primary);
		border-bottom: 1px solid var(--border);
		padding: 1rem 0;
		box-shadow: var(--shadow-sm);
	}

	.container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 1.5rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.nav-brand h2 {
		margin: 0;
		color: var(--text-primary);
		font-size: 1.5rem;
	}

	.nav-items {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.user-info {
		color: var(--text-secondary);
	}

	.btn {
		padding: 0.5rem 1rem;
		border-radius: var(--radius);
		font-weight: 500;
		transition: all 0.2s;
	}

	.btn-secondary {
		background-color: var(--bg-tertiary);
		color: var(--text-primary);
	}

	.btn-secondary:hover {
		background-color: var(--secondary);
		color: white;
	}

	main {
		min-height: calc(100vh - 80px);
	}
</style>
