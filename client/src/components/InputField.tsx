import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useState } from 'react';
import { uploadFile } from '../services/Requests';

const VisuallyHiddenInput = styled('input')({
  height: 1,
  width: 1,
});

export default function InputFile(props: { theme: string }) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    
    if (files && files.length > 0) {
      setSelectedFile(files[0]);
    }

    if (selectedFile) {
      uploadFile(selectedFile);
    } else {
      alert('Error uploading file');
    }
  }

  return (
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
        '&:hover': {
            backgroundColor: "#FFAE00",
            borderColor: 'none',
            boxShadow: 'none',
        },
      }}
      
    >
      Upload file
      <VisuallyHiddenInput type="file" onChange={handleUpload}/>
    </Button>
  );
}
