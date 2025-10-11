<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { authStore } from '$lib/auth';
	import { api } from '$lib/api';

	let mode: 'login' | 'register' = $state('login');
	let username = $state('');
	let password = $state('');
	let loading = $state(false);
	let error: string | null = $state(null);
	let showPassword = $state(false);

	onMount(() => {
		if ($authStore.token) {
			goto('/dashboard');
		}
	});

	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		error = null;

		try {
			if (mode === 'register') {
				await api.register({ username, password });
				mode = 'login';
				username = '';
				password = '';
				error = 'Account created! Please log in.';
			} else {
				const response = await api.login({ username, password });
				// Save token first so subsequent API calls can use it
				authStore.login(response.token, { id: 0, username: '', balance: 0 });
				// Now fetch the user data with the token in place
				const user = await api.getMe();
				authStore.updateUser(user);
				goto('/dashboard');
			}
		} catch (e) {
			error = e instanceof Error ? e.message : 'An error occurred';
		} finally {
			loading = false;
		}
	}
</script>

<div class="auth-container">
	<div class="auth-card">
		<div class="auth-header">
			<h1>🏦 WOOF Bank</h1>
			<p class="subtitle">Modern Banking Made SECURE</p>
		</div>

		<div class="tab-buttons">
			<button 
				class="tab-btn" 
				class:active={mode === 'login'}
				onclick={() => { mode = 'login'; error = null; }}
			>
				Login
			</button>
			<button 
				class="tab-btn" 
				class:active={mode === 'register'}
				onclick={() => { mode = 'register'; error = null; }}
			>
				Register
			</button>
		</div>

		{#if error}
			<div class="alert" class:success={mode === 'login' && error.includes('created')}>
				{error}
			</div>
		{/if}

		<form onsubmit={handleSubmit}>
			<div class="form-group">
				<label for="username">Username</label>
				<input
					id="username"
					type="text"
					bind:value={username}
					placeholder="Enter your username"
					required
					disabled={loading}
				/>
			</div>

			<div class="form-group">
				<label for="password">Password</label>
				<div class="password-input-wrapper">
					<input
						id="password"
						type={showPassword ? 'text' : 'password'}
						bind:value={password}
						placeholder="Enter your password"
						required
						disabled={loading}
					/>
					<button
						type="button"
						class="password-toggle"
						onclick={() => (showPassword = !showPassword)}
						disabled={loading}
					>
						{showPassword ? '👁️' : '👁️‍🗨️'}
					</button>
				</div>
			</div>

			<button type="submit" class="btn btn-primary" disabled={loading}>
				{#if loading}
					Processing...
				{:else}
					{mode === 'login' ? 'Login' : 'Create Account'}
				{/if}
			</button>
		</form>
	</div>
</div>

<style>
	.auth-container {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 1.5rem;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	}

	.auth-card {
		background: var(--bg-primary);
		border-radius: var(--radius-lg);
		box-shadow: var(--shadow-lg);
		padding: 2.5rem;
		width: 100%;
		max-width: 420px;
	}

	.auth-header {
		text-align: center;
		margin-bottom: 2rem;
	}

	.auth-header h1 {
		color: var(--text-primary);
		margin-bottom: 0.5rem;
	}

	.subtitle {
		color: var(--text-muted);
		font-size: 0.95rem;
	}

	.tab-buttons {
		display: flex;
		gap: 0.5rem;
		margin-bottom: 2rem;
		background: var(--bg-tertiary);
		padding: 0.25rem;
		border-radius: var(--radius);
	}

	.tab-btn {
		flex: 1;
		padding: 0.625rem;
		background: transparent;
		color: var(--text-secondary);
		font-weight: 500;
		border-radius: var(--radius-sm);
		transition: all 0.2s;
	}

	.tab-btn.active {
		background: var(--bg-primary);
		color: var(--primary);
		box-shadow: var(--shadow-sm);
	}

	.alert {
		padding: 0.875rem;
		border-radius: var(--radius);
		margin-bottom: 1.5rem;
		background-color: #fee2e2;
		color: #991b1b;
		font-size: 0.875rem;
	}

	.alert.success {
		background-color: #d1fae5;
		color: #065f46;
	}

	form {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.form-group {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	label {
		font-weight: 500;
		color: var(--text-primary);
		font-size: 0.875rem;
	}

	.password-input-wrapper {
		position: relative;
		display: flex;
		align-items: center;
	}

	.password-input-wrapper input {
		flex: 1;
		padding-right: 3rem;
	}

	.password-toggle {
		position: absolute;
		right: 0.5rem;
		background: none;
		border: none;
		padding: 0.5rem;
		cursor: pointer;
		font-size: 1.25rem;
		opacity: 0.6;
		transition: opacity 0.2s;
	}

	.password-toggle:hover:not(:disabled) {
		opacity: 1;
	}

	.password-toggle:disabled {
		cursor: not-allowed;
		opacity: 0.3;
	}

	input {
		padding: 0.75rem 1rem;
		border: 1px solid var(--border);
		border-radius: var(--radius);
		font-size: 1rem;
		transition: all 0.2s;
		background: var(--bg-primary);
	}

	input:focus {
		outline: none;
		border-color: var(--primary);
		box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
	}

	input:disabled {
		background: var(--bg-tertiary);
		cursor: not-allowed;
	}

	.btn {
		padding: 0.875rem 1.5rem;
		border-radius: var(--radius);
		font-weight: 600;
		font-size: 1rem;
		transition: all 0.2s;
	}

	.btn-primary {
		background: var(--primary);
		color: white;
	}

	.btn-primary:hover:not(:disabled) {
		background: var(--primary-hover);
		transform: translateY(-1px);
		box-shadow: var(--shadow-md);
	}

	.btn-primary:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
</style>
