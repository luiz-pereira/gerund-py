import React from 'react';
import { Grid, TextField } from '@mui/material';

export default function Home() {
  return (
    <Grid container direction={'column'}>
      <TextField
        id="outlined-multiline-static"
        label="Prompt"
        multiline
        rows={4}
        style={{ width: '50%', margin: 10 }}
      />
      <TextField
        id="outlined-multiline-static"
        label="Company Presentation"
        multiline
        rows={4}
        style={{ width: '50%', margin: 10 }}
      />
      <TextField
        id="outlined-multiline-static"
        label="New Product"
        multiline
        rows={4}
        style={{ width: '50%', margin: 10 }}
      />
    </Grid>
  );
}
