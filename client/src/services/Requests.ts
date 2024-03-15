import axios from "axios";
import { environment } from "../environment/environment";

export async function fetchInformation(
  input: string
): Promise<string | undefined> {
  if (!input) return;

  try {
    const response = await axios.post(`${environment.serverUrl}/submit`, {
      query: input,
    });
    return response.data;
  } catch (error) {
    console.error("Error submitting query:", error);
  }

  return "";
}

export async function uploadFile(input: File): Promise<void> {
  const formData = new FormData();
  formData.append("file", input);

  const response = await axios.post(
    `${environment.serverUrl}/upload`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  console.log("File uploaded successfully:", response.data);
}
