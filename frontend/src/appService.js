import axios from 'axios';

export const predict = async (data) => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/predict', data);
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export const getHistory = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:5000/history');
        return response.data;
    } catch (error) {
        console.error(error);
    }
}