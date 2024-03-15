import axios from 'axios';
import { environment } from '../environment/environment';

export async function fetchInformation(input: string): Promise<string> {
    try {

    } catch {

    }

    return '';
}



export async function uploadFile(input: File) : Promise<void> {
    try {
        const formData = new FormData();
        formData.append('file', input);

        const response = await axios.post(`${environment.serverUrl}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        alert('Successfully uploaded your file');
        console.log('File uploaded successfully:', response.data);
    } catch (error) {
        console.error('Error uploading file:', error);
    }
}


