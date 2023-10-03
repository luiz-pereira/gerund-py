import React, {useEffect, useState} from 'react';
import { Grid, TextField, Button, Box, CircularProgress } from '@mui/material';
import { get, post, patch } from '../../api/apis'
import { useParams } from 'react-router-dom'
import ListQuestions from './questions/ListQuestions'
import ShowQuestion from './questions/ShowQuestion'

export default function Script() {
  const [name, setName] = useState('');
  const [customPrompt, setCustomPrompt] = useState('');
  const [presentation, setPresentation] = useState('');
  const [newProduct, setNewProduct] = useState('');
  const [loading, setLoading] = useState(false);
  const [script, setScript] = useState(null);
  const [selectedQuestionId, setSelectedQuestionId] = useState(null)
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

  const handleGenerateAllQuestionVariations = async () => {
    setLoading(true)
    const scriptResponse = await post(`scripts/${id}/generate_questions_variations`)
    setValues(scriptResponse)
    setLoading(false)
  }



  useEffect(() => {
    fetchScript()
  }, [])

  const handleSaveChanges = async () => {
    setLoading(true)
    const scriptResponse = await patch("scripts", id, {name, customPrompt, presentation, newProduct})
    if (scriptResponse.error) {
      console.log("error")
      return
    }
    setLoading(false)
    setValues(scriptResponse)
  }

  const handleQuestionClick = (questionId) => {
    setSelectedQuestionId(questionId)
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
          onChange={(e) => setName(e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="Prompt"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={customPrompt}
          disabled={loading}
          onChange={(e) => setCustomPrompt(e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="Company Presentation"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={presentation}
          disabled={loading}
          onChange={(e) => setPresentation(e.target.value)}
        />
        <TextField
          id="outlined-multiline-static"
          label="New Product"
          multiline
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={newProduct}
          disabled={loading}
          onChange={(e) => setNewProduct(e.target.value)}
        />
      </Grid>
        <Button
          variant="contained"
          color='warning'
          style={{ margin: 10 }}
          onClick={handleSaveChanges}
          disabled={loading}
        >
          {loading ? <Box><CircularProgress size={12}/>Generating...</Box> : "Save Changes"}
        </Button>
        <Button
          variant="contained"
          style={{ margin: 10 }}
          onClick={handleGenerateQuestion}
          disabled={loading}
        >
          {loading ? <Box><CircularProgress size={12}/>Generating...</Box> : "Generate Questions"}
        </Button>
        <Button
          variant="contained"
          color='secondary'
          style={{ margin: 10 }}
          onClick={handleGenerateAnswer}
          disabled={loading}
          >
            {loading ? <Box><CircularProgress size={12}/>Generating...</Box> : "Generate Answers"}
          </Button>
          <Button
            variant="contained"
            color="error"
            style={{ margin: 10 }}
            onClick={handleGenerateAllQuestionVariations}
            disabled={loading}
          >
            {loading ? <Box><CircularProgress size={12}/>Generating...</Box> : "Generate Question Variations"}
          </Button>
        <ListQuestions questions={script?.questions || []} handleQuestionClick={handleQuestionClick} fetchScript={fetchScript}/>
        <ShowQuestion questionId={selectedQuestionId} open={!!selectedQuestionId} handleClose={() => setSelectedQuestionId(null)}/>
    </Grid>
  );
}
