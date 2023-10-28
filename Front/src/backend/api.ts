import axios from 'axios';

const baseURL = 'https://127.0.0.1:8000'

export const client = axios.create({
    baseURL: baseURL,
});