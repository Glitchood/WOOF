<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { authStore, api } from '$lib';


  let mode: 'login' | 'register' = 'login';
  let username = '';
  let password = '';
  let loading = false;
  let error: string | null = null;

  onMount(() => {
    authStore.init();
  });

  async function handleSubmit() {
    loading = true;
    error = null;
    
    try {
      if (mode === 'register') {
        const response = await api.register({ username, password });
        //alert(response.message);
        mode = 'login';
      } else {
        const response = await api.login({ username, password });
        console.log(response.token);
        const userResponse = await api.getMe(response.token);
        authStore.login({
          userId: userResponse.userId,
          username: userResponse.username,
          token: response.token
        });
        goto('/dashboard');
      }
    } catch (e) {
      error = e instanceof Error ? e.message : 'An error occurred';
    } finally {
      loading = false;
    }
  }
</script>

<div class="container">
  <div class="card">
    <h1>{mode === 'login' ? 'Login' : 'Register'}</h1>

    {#if error}
      <div class="error">{error}</div>
    {/if}

    <form on:submit|preventDefault={handleSubmit}>
      <input
        type="text"
        placeholder="Username"
        bind:value={username}
        required
      />
      <input
        type="password"
        placeholder="Password"
        bind:value={password}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Processing...' : mode === 'login' ? 'Login' : 'Register'}
      </button>
    </form>

    <p class="toggle">
      {mode === 'login' ? "Don't have an account?" : 'Already have an account?'}
      <button class="link" on:click={() => (mode = mode === 'login' ? 'register' : 'login')}>
        {mode === 'login' ? 'Register' : 'Login'}
      </button>
    </p>
  </div>
</div>

<style>
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }

  .card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    width: 100%;
    max-width: 400px;
  }

  h1 {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  input {
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
  }

  button[type="submit"] {
    background: #667eea;
    color: white;
    padding: 0.75rem;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s;
  }

  button[type="submit"]:hover {
    background: #5568d3;
  }

  button[type="submit"]:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .toggle {
    text-align: center;
    margin-top: 1rem;
    color: #666;
  }

  .link {
    background: none;
    border: none;
    color: #667eea;
    cursor: pointer;
    text-decoration: underline;
    padding: 0;
    margin-left: 0.25rem;
  }

  .error {
    background: #ffebee;
    color: #c62828;
    padding: 0.75rem;
    border-radius: 6px;
    margin-bottom: 1rem;
  }
</style>
