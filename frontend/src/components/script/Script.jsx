import React, {useEffect, useState} from 'react';
import { Grid, TextField, Button, Box, CircularProgress } from '@mui/material';
import { get, post, patch } from '../../api/apis'
import { useParams } from 'react-router-dom'
import ListQuestions from './questions/ListQuestions'

export default function Script() {
  const [name, setName] = useState('');
  const [customPrompt, setCustomPrompt] = useState('');
  const [presentation, setPresentation] = useState('');
  const [newProduct, setNewProduct] = useState('');
  const [loading, setLoading] = useState(false);
  const [script, setScript] = useState(null);
  const { id } = useParams();


  const fetchScript = async () => {
    const scriptResponse = await get("scripts/" + id)
    setValues(scriptResponse)
  }

  const setValues = (scriptResponse) => {
    setScript(scriptResponse)
    setName(scriptResponse.name)
    setCustomPrompt(scriptResponse.custom_prompt)
    setPresentation(scriptResponse.presentation)
    setNewProduct(scriptResponse.new_product)
  }

  const handleGenerateQuestion = async () => {
    setLoading(true)
    const scriptResponse = await post(`scripts/${id}/generate_questions`)
    setValues(scriptResponse)
    setLoading(false)
  }

  const handleGenerateAnswer = async () => {
    setLoading(true)
    const scriptResponse = await post(`scripts/${id}/generate_answers`)
    setValues(scriptResponse)
    setLoading(false)
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
          disabled={loading}
          onChange={(e) => handleChange("name", e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="Prompt"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={customPrompt}
          disabled={loading}
          onChange={(e) => handleChange("customPrompt", e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="Company Presentation"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={presentation}
          disabled={loading}
          onChange={(e) => handleChange("presentation", e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="New Product"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={newProduct}
          disabled={loading}
          onChange={(e) => handleChange("newProduct", e.target.value)}
        />
      </Grid>
        <Button
          variant="contained"
          style={{ margin: 10 }}
          onClick={handleGenerateQuestion}
          disabled={loading}
        >
          {loading? <Box><CircularProgress size={12}/>Generating...</Box> : "Generate Questions"}
        </Button>
        <Button
          variant="contained"
          color='secondary'
          style={{ margin: 10 }}
          onClick={handleGenerateAnswer}
          disabled={loading}
          >
            {loading? <Box><CircularProgress size={12}/>Generating...</Box> : "Generate Answers"}
          </Button>
        <ListQuestions questions={script?.question_set || []} />
    </Grid>
  );
}