import { authStore } from '$lib';
import { get } from 'svelte/store';

const API_ROOT_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface ErrorResponse {
	detail?: string;
}

async function handleResponse<T>(response: Response): Promise<T> {
	if (!response.ok) {
		const error: ErrorResponse = await response.json().catch(() => ({}));
		throw new Error(error.detail || 'An error occurred');
	}
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
	toUsername: string;
	amount: number;
	description: string;
}

//Responses
export interface UserResponse {
	id: number;
	username: string;
	balance: number;
}

export interface LoginResponse {
	token: string;
}

export interface Transaction {
	id: number;
	from_user_id: number;
	to_user_id: number;
	amount: number;
	description: string;
}

export interface TransactionResponse {
	status: string;
	transaction_id: number;
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
		return handleResponse<LoginResponse>(response);
	},

	async getMe(): Promise<UserResponse> {
		const response = await fetch(`${API_ROOT_URL}/api/me`, {
			headers: getAuthHeaders()
		});
		return handleResponse<UserResponse>(response);
	},

	async getUser(userId: number): Promise<UserResponse> {
		const response = await fetch(`${API_ROOT_URL}/api/users/${userId}`, {
			headers: getAuthHeaders()
		});
		return handleResponse<UserResponse>(response);
	},

	async createTransaction(transaction: TransactionCreate): Promise<TransactionResponse> {
		const response = await fetch(`${API_ROOT_URL}/api/transactions`, {
			method: 'POST',
			headers: getAuthHeaders(),
			body: JSON.stringify(transaction)
		});
		return handleResponse<TransactionResponse>(response);
	},

	async getTransactions(userId: number): Promise<Transaction[]> {
		const response = await fetch(`${API_ROOT_URL}/api/users/${userId}/transactions`, {
			headers: getAuthHeaders()
		});
		return handleResponse<Transaction[]>(response);
	}
};
