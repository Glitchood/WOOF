import { authStore } from '$lib';
import { get } from 'svelte/store';

const API_ROOT_URL = 'http://localhost:8000';

interface ErrorResponse {
	detail?: string;
}

async function handleResponse<T>(response: Response): Promise<t> {
	if (!response.ok) {
		const error: ErrorResponse = await response.json().catch(() => ({}));
		throw new Error(error.detail || 'An error occured');
	}
	//console.log(response.json());
	return response.json();
}

function getAuthHeaders(): HeadersInit {
	const token = get(authStore)?.token;

	return {
		'Content-Type': 'application/json',
		...(token && { Authorization: `Bearer ${token}` })
	};
}

// Type Defs

//Requests
export interface UserRegister {
	//used for both register and login
	username: string;
	password: string;
}

export interface DeleteAccountRequest {
	username: string;
	password: string;
}

export interface TransactionCreate {
	fromUserId: number;
	toUsername: string;
	amount: number;
	description: string;
}

//Responses
export interface UserResponse {
	userId: number;
	username: string;
	message?: string;
}

export interface MeResponse {
	userId: number;
	username: string;
	balance: number;
}

export interface LoginResponse {
	token: string;
}

export interface AccountResponse {
	userId: number;
	balance: number;
}

export interface Transaction {
	transactionId: number;
	amount: number;
	description: string;
}

export interface TransactionResponse {
	status: string;
	transactionId: number;
}

export const api = {
	async register(user: UserRegister): Promise<UserResponse> {
		const response = await fetch(`${API_ROOT_URL}/api/register`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(user)
		});
		return handleResponse<UserResponse>(response);
	},

	async login(user: UserRegister): Promise<LoginResponse> {
		const response = await fetch(`${API_ROOT_URL}/api/login`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(user)
		});
		console.log('Token: ', get(authStore)?.token);
		return handleResponse<LoginResponse>(response);
	},

	async deleteAccount(username: string, password: string): Promise<{ status: string }> {
		const response = await fetch(`${API_ROOT_URL}/api/accounts`, {
			method: 'POST',
			headers: getAuthHeaders(),
			body: JSON.stringify({ username, password })
		});
		return handleResponse<{ status: string }>(response);
	},

	async getMe(token: string): Promise<{ userId: number; username: string }> {
		console.log('token: ', token);
		console.log(`Bearer ${token}`);
		const response = await fetch(`${API_ROOT_URL}/api/me`, {
			headers: { Authorization: `Bearer ${token}` }
		});
		return handleResponse<{ userId: number; username: string; balance: number }>(response);
	},

	async transferFunds(transaction: TransactionCreate): Promise<TransactionResponse> {
		const response = await fetch(`${API_ROOT_URL}/api/transactions`, {
			method: 'POST',
			headers: getAuthHeaders(),
			body: JSON.stringify(transaction)
		});
		return handleResponse<TransactionResponse>(response);
	},

	async getTransactions(userId: number): Promise<Transaction[]> {
		const response = await fetch(`${API_ROOT_URL}/api/accounts/${userId}/transactions`, {
			headers: getAuthHeaders()
		});
		return handleResponse<Transaction[]>(response);
	},

	async searchTransactions(userId: number, description: string): Promise<Transaction[]> {
		const response = await fetch(
			`${API_ROOT_URL}/api/accounts/${userId}/transactions/search?description=${encodeURIComponent(description)}`,
			{ headers: getAuthHeaders() }
		);
		return handleResponse<Transaction[]>(response);
	}
};
