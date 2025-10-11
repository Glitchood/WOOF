import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export interface AuthState {
	token: string | null;
	user: {
		id: number;
		username: string;
		balance: number;
	} | null;
}

const initialState: AuthState = {
	token: browser ? localStorage.getItem('token') : null,
	user: browser && localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null
};

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>(initialState);

	return {
		subscribe,
		login: (token: string, user: { id: number; username: string; balance: number }) => {
			if (browser) {
				localStorage.setItem('token', token);
				localStorage.setItem('user', JSON.stringify(user));
			}
			set({ token, user });
		},
		updateUser: (user: { id: number; username: string; balance: number }) => {
			if (browser) {
				localStorage.setItem('user', JSON.stringify(user));
			}
			update((state) => ({ ...state, user }));
		},
		logout: () => {
			if (browser) {
				localStorage.removeItem('token');
				localStorage.removeItem('user');
			}
			set({ token: null, user: null });
		}
	};
}

export const authStore = createAuthStore();
