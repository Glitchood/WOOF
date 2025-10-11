import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface User {
	userId: number;
	username: string;
	token: string;
}

function createAuthStore() {
	const { subscribe, set, update } = writable<User | null>(null);

	return {
		subscribe,
		login: (user: User) => {
			if (browser) {
				localStorage.setItem('token', user.token);
				localStorage.setItem(
					'user',
					JSON.stringify({ userId: user.userId, username: user.username })
				);
			}
			set(user);
		},
		logout: () => {
			if (browser) {
				localStorage.removeItem('token');
				localStorage.removeItem('user');
			}
			set(null);
		},
		init: () => {
			if (browser) {
				const token = localStorage.getItem('token');
				const userStr = localStorage.getItem('user');
				if (token && userStr) {
					const user = JSON.parse(userStr);
					set({ ...user, token });
				}
			}
		}
	};
}

export const authStore = createAuthStore();
