import * as React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const VisuallyHiddenInput = styled('input')({
  height: 1,
  width: 1,
});

export default function InputFile(props: { theme: string }) {
  return (
    <Button
      component="label"
      role={undefined}
      variant="contained"
      tabIndex={-1}
      startIcon={<CloudUploadIcon />}
      sx={{
        backgroundColor: "#FFAE00",
        borderRadius: 3,
        borderShadow: 3,
      }}
    >
      Upload file
      <VisuallyHiddenInput type="file" />
    </Button>
  );
}
