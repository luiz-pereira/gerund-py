import React, { useEffect, useState } from 'react'
import { Grid, TextField, Button, Box, CircularProgress } from '@mui/material'
import KeyboardDoubleArrowRightIcon from '@mui/icons-material/KeyboardDoubleArrowRight'
import { useParams } from 'react-router-dom'
import ListQuestions from './questions/ListQuestions'
import ShowQuestion from './questions/ShowQuestion'
import { get, post, patch } from '../../api/apis'
import ShowAnswer from './questions/ShowAnswer'

export default function Script () {
  const [name, setName] = useState('')
  const [customPrompt, setCustomPrompt] = useState('')
  const [presentation, setPresentation] = useState('')
  const [newProduct, setNewProduct] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedQuestionId, setSelectedQuestionId] = useState(null)
  const [selectedAnswerId, setSelectedAnswerId] = useState(null)
  const [questions, setQuestions] = useState([])

  const { id } = useParams()

  const setValues = (scriptResponse) => {
    setName(scriptResponse.name)
    setCustomPrompt(scriptResponse.custom_prompt)
    setPresentation(scriptResponse.presentation)
    setNewProduct(scriptResponse.new_product)
  }

  const fetchScript = async () => {
    const scriptResponse = await get(`scripts/${id}`)
    setValues(scriptResponse)
  }

  const fetchQuestions = async () => {
    const questionsResponse = await get(`scripts/${id}/questions`)
    setQuestions(questionsResponse)
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

  const handleGenerateAllAnswerVariations = async () => {
    setLoading(true)
    const scriptResponse = await post(`scripts/${id}/generate_answers_variations`)
    setValues(scriptResponse)
    setLoading(false)
  }

  useEffect(() => {
    fetchScript()
    fetchQuestions()
  }, [])

  const handleSaveChanges = async () => {
    setLoading(true)
    const scriptResponse = await patch('scripts', id, { name, customPrompt, presentation, newProduct })
    if (scriptResponse.error) {
      console.log('error')
      return
    }
    setLoading(false)
    setValues(scriptResponse)
  }

  return (
    <Grid container>
      <Grid container direction="column">
        <TextField
          id="outlined-multiline-static"
          label="Name"
          rows={4}
          style={{ width: '50%', margin: 10 }}
          value={name}
          disabled={loading}
          onBlur={handleSaveChanges}
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
          onBlur={handleSaveChanges}
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
          onBlur={handleSaveChanges}
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
          onBlur={handleSaveChanges}
          onChange={(e) => setNewProduct(e.target.value)}
        />
      </Grid>
      <Grid container direction="row" alignItems="center">
        <Button
          variant="contained"
          style={{ margin: 10 }}
          onClick={handleGenerateQuestion}
          disabled={loading}
        >
          {loading
            ? (
            <Box>
              <CircularProgress size={12} />
              Generating...
            </Box>
              )
            : 'Generate Questions'}
        </Button>
        <KeyboardDoubleArrowRightIcon />
        <Button
          variant="contained"
          color="error"
          style={{ margin: 10 }}
          onClick={handleGenerateAllQuestionVariations}
          disabled={loading}
        >
          {loading
            ? (
            <Box>
              <CircularProgress size={12} />
              Generating...
            </Box>
              )
            : 'Generate Question Variations'}
        </Button>
        <KeyboardDoubleArrowRightIcon />
        <Button
          variant="contained"
          color="secondary"
          style={{ margin: 10 }}
          onClick={handleGenerateAnswer}
          disabled={loading}
        >
          {loading
            ? (
            <Box>
              <CircularProgress size={12} />
              Generating...
            </Box>
              )
            : 'Generate Answers'}
        </Button>
        <KeyboardDoubleArrowRightIcon />
        <Button
          variant="contained"
          color="warning"
          style={{ margin: 10 }}
          onClick={handleGenerateAllAnswerVariations}
          disabled={loading}
        >
          {loading
            ? (
            <Box>
              <CircularProgress size={12} />
              Generating...
            </Box>
              )
            : 'Generate Answer Variations'}
        </Button>
      </Grid>
      <ListQuestions
        questions={questions}
        handleAnswerClick={setSelectedAnswerId}
        handleQuestionClick={setSelectedQuestionId}
        fetchScript={fetchScript}
      />
      <ShowQuestion questionId={selectedQuestionId} open={!!selectedQuestionId} handleClose={() => setSelectedQuestionId(null)} />
      <ShowAnswer answerId={selectedAnswerId} open={!!selectedAnswerId} handleClose={() => setSelectedAnswerId(null)} />
    </Grid>
  )
}
