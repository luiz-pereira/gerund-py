import React, {useEffect, useState} from 'react';
import { Button, Grid, TextField } from '@mui/material';
import { get, patch } from '../../api/apis'
import { useParams } from 'react-router-dom'

export default function Script() {
  const [name, setName] = useState('');
  const [customPrompt, setCustomPrompt] = useState('');
  const [presentation, setPresentation] = useState('');
  const [newProduct, setNewProduct] = useState('');
  const { id } = useParams();


  const fetchScript = async () => {
    const scriptResponse = await get("scripts/" + id)
    setValues(scriptResponse)
  }

  const setValues = (scriptResponse) => {
    setName(scriptResponse.name)
    setCustomPrompt(scriptResponse.custom_prompt)
    setPresentation(scriptResponse.presentation)
    setNewProduct(scriptResponse.new_product)
  }

  useEffect(() => {
    fetchScript()
  }, [])

  const handleChange = async (key, value) => {
    const scriptResponse = await patch("scripts", id, {[key]: value})
    if (scriptResponse.error) {
      console.log("error")
      return
    }
    setValues(scriptResponse)
  }


  return (
    <Grid container>
      <Grid container direction={'column'}>
      <TextField
          id="outlined-multiline-static"
          label="Name"
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={name}
          onChange={(e) => handleChange("name", e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="Prompt"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={customPrompt}
          onChange={(e) => handleChange("customPrompt", e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="Company Presentation"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={presentation}
          onChange={(e) => handleChange("presentation", e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="New Product"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={newProduct}
          onChange={(e) => handleChange("newProduct", e.target.value)}
        />
      </Grid>
      <Grid item>
        <Button variant="contained" style={{ margin: 10 }} onClick={()=> console.log("whatevis")}>Generate</Button>
      </Grid>
    </Grid>
  );
}
