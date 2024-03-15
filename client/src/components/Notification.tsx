import * as React from 'react';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

export default function CustomizedSnackbars(props: {
  text: string
  severity: string
}) {
  const [open, setOpen] = React.useState(true);

  const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
  };

  return (
    <div>
      <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert
          onClose={handleClose}
          severity={props.severity as "success" | "info" | "warning" | "error" | undefined}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {props.text}
        </Alert>
      </Snackbar>
    </div>
  );
}