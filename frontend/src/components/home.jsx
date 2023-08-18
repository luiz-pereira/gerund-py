import React from 'react';
import { Button, Container, Grid, TextField } from '@mui/material';


export default function Home() {
  return (
    <Container
      container
      direction="column"
      justifyContent="space-evenly"
      alignItems="flex-start"
    >
      <TextField
        id="outlined-multiline-static"
        label="Multiline"
        multiline
        rows={4}
        defaultValue="Default Value"
        />
        <TextField
        id="outlined-multiline-static"
        label="Multiline"
        multiline
        rows={4}
        defaultValue="Default Value"
        />
      <Button>Click me</Button>
    </Container>
  );
}
