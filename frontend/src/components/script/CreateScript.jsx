import React, {useEffect, useState} from 'react';
import { Button, Grid, TextField } from '@mui/material';
import { get, post } from '../../api/apis'

export default function Home() {
  const [name, setName] = useState('');
  const [prompt, setPrompt] = useState('');
  const [presentation, setPresentation] = useState('');
  const [newProduct, setNewProduct] = useState('');

  const onClickGenerate = async () => {
    const response = await post('/generate', {
      prompt: prompt,
      company_presentation: presentation,
      new_product: newProduct
    });
    console.log(response);
    debugger;
  };

  return (
    <Grid container>
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
      <Grid item>
        <Button variant="contained" style={{ margin: 10 }} onClick={onClickGenerate}>Generate</Button>
      </Grid>
    </Grid>
  );
}
