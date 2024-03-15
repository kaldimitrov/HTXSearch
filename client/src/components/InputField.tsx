import { styled } from "@mui/material/styles";
import Button from "@mui/material/Button";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { uploadFile } from "../services/Requests";
import CustomNotification from "./Notification";
import { useState } from "react";

const VisuallyHiddenInput = styled("input")({
  height: 1,
  width: 1,
});

export default function InputFile(props: { theme: string }) {
  const [notification, setNotification] = useState<string | null>(null);
  const [severity, setSeverity] = useState<string | undefined>("success");

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;

    if (files && files.length > 0) {
      try {
        const response = await uploadFile(files[0]);
        setNotification("Successfully uploaded file!");
        setSeverity("success");
        console.log("File uploaded successfully:", response);
      } catch (error) {
        setNotification("Error uploading file!");
        setSeverity("error");
        console.error("Error uploading file:", error);
      }
    }
  };

  const closeNotification = () => {
    setNotification(null);
  };

  return (
    <>
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<CloudUploadIcon />}
        color="secondary"
        sx={{
          backgroundColor: "#FFAE00",
          borderRadius: 3,
          borderShadow: 3,
          "&:hover": {
            backgroundColor: "#FFAE00",
            borderColor: "none",
            boxShadow: "none",
          },
        }}
      >
        Upload file
        <VisuallyHiddenInput type="file" name="file" onChange={handleUpload} />
      </Button>
      <div>
        {notification && (
          <div>
            <CustomNotification text={notification!} severity={severity!} />
          </div>
        )}
      </div>
    </>
  );
}
