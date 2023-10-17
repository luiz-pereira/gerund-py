import React, { useEffect, useState } from 'react'
import { TextField, Button, Box, CircularProgress, Container, Card } from '@mui/material'
import KeyboardDoubleArrowRightIcon from '@mui/icons-material/KeyboardDoubleArrowRight'
import { useParams } from 'react-router-dom'
import ListQuestions from './questions/ListQuestions'
import ShowQuestion from './questions/ShowQuestion'
import { get, post, patch } from '../../api/apis'
import ShowAnswer from './questions/ShowAnswer'
import Grid2 from '@mui/material/Unstable_Grid2/Grid2'
import { grey } from '@mui/material/colors'
import ShowScriptContents from './ShowScriptContents'

export default function Script () {
  const [name, setName] = useState('')
  const [customPrompt, setCustomPrompt] = useState('')
  const [presentation, setPresentation] = useState('')
  const [newProduct, setNewProduct] = useState('')
  const [loading, setLoading] = useState(false)
  const [selectedQuestionId, setSelectedQuestionId] = useState(null)
  const [selectedAnswerId, setSelectedAnswerId] = useState(null)
  const [questions, setQuestions] = useState([])
  const [entityName, setEntityName] = useState(null)

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

  const handleGenerateEmbeddings = async () => {
    setLoading(true)
    await post(`scripts/${id}/fill_embeddings`)
    setLoading(false)
  }

  const handleGenerateSpeeches = async () => {
    setLoading(true)
    await post(`scripts/${id}/fill_speeches`)
    setLoading(false)
  }

  const handleStartModeration = async () => {
    setLoading(true)
    await get(`scripts/${id}/start_moderation`)
    setLoading(false)
  }

  return (
    <Container maxWidth="100%">
      <Grid2 container direction="row">
        <Grid2 container direction="column" xs={6}>
          <TextField
            id="outlined-multiline-static"
            label="Name"
            rows={4}
            style={{ width: 'fit-content', margin: 10 }}
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
            style={{ width: '90%', margin: 10 }}
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
            style={{ width: '90%', margin: 10 }}
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
            style={{ width: '90%', margin: 10 }}
            value={newProduct}
            disabled={loading}
            onBlur={handleSaveChanges}
            onChange={(e) => setNewProduct(e.target.value)}
          />
        </Grid2>
        <Grid2 container direction={'column'} xs={6} alignItems="center">
          <Grid2 item>
            <Card style={{ margin: 10, padding: 10 }}>
              <Button
                variant="contained"
                style={{ margin: 10, backgroundColor: grey[500] }}
                onClick={() => setEntityName('initial_pitches')}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Initial Pitches'}
              </Button>
            </Card>
          </Grid2>
          <Grid2 item>
            <Card style={{ margin: 10, padding: 10 }}>
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
                variant="outlined"
                color="primary"
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
            </Card>
          </Grid2>
          <Grid2 item>
            <Card style={{ margin: 10, padding: 10 }}>
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
                variant="outlined"
                color="secondary"
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
            </Card>
          </Grid2>
          <Grid2 item>
            <Card style={{ margin: 10, padding: 10 }}>
              <Button
                variant="contained"
                color="success"
                style={{ margin: 10 }}
                onClick={() => setEntityName('success_triggers')}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Success Triggers'}
              </Button>
              <KeyboardDoubleArrowRightIcon />
              <Button
                variant="outlined"
                color="success"
                style={{ margin: 10 }}
                onClick={() => setEntityName('success_endings')}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Success Endings'}
              </Button>
            </Card>
          </Grid2>
          <Grid2 item>
            <Card style={{ margin: 10, padding: 10 }}>
              <Button
                variant="contained"
                color="warning"
                style={{ margin: 10 }}
                onClick={() => setEntityName('partial_fail_triggers')}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Partial Fail Triggers'}
              </Button>
              <KeyboardDoubleArrowRightIcon />
              <Button
                variant="outlined"
                color="warning"
                style={{ margin: 10 }}
                onClick={() => setEntityName('intermediate_pitches')}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Intermediate Pitches'}
              </Button>
            </Card>
          </Grid2>
          <Grid2 item>
            <Card style={{ margin: 10, padding: 10 }}>
              <Button
                variant="contained"
                color="error"
                style={{ margin: 10 }}
                onClick={() => setEntityName('total_fail_triggers')}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Fail Triggers'}
              </Button>
              <KeyboardDoubleArrowRightIcon />
              <Button
                variant="outlined"
                color="error"
                style={{ margin: 10 }}
                onClick={() => setEntityName('fail_endings')}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Fail Endings'}
              </Button>
            </Card>
          </Grid2>
          <Grid2 item>
            <Card style={{ margin: 10, padding: 10 }}>
              <Button
                variant="contained"
                style={{ margin: 10, backgroundColor: grey[500] }}
                onClick={() => setEntityName('stallings')}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Stallings'}
              </Button>
            </Card>
          </Grid2>
          <Grid2 item>
            <Card style={{ margin: 10, padding: 10 }}>
              <Button
                variant="contained"
                color="success"
                style={{ margin: 10 }}
                onClick={handleGenerateEmbeddings}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Fill Embeddings'}
              </Button>
              <KeyboardDoubleArrowRightIcon />
              <Button
                variant="outlined"
                color="success"
                style={{ margin: 10 }}
                onClick={handleGenerateSpeeches}
                disabled={loading}
              >
                {loading
                  ? (
                  <Box>
                    <CircularProgress size={12} />
                    Generating...
                  </Box>
                    )
                  : 'Fill Speeches'}
              </Button>
            </Card>
          </Grid2>
        </Grid2>
      </Grid2>
      <Button variant="contained" color="primary" style={{ margin: 10 }} onClick={handleStartModeration}>
        Start Moderation
      </Button>
      <ListQuestions
        questions={questions}
        handleAnswerClick={setSelectedAnswerId}
        handleQuestionClick={setSelectedQuestionId}
        fetchScript={fetchScript}
      />
      <ShowQuestion questionId={selectedQuestionId} open={!!selectedQuestionId} handleClose={() => setSelectedQuestionId(null)} />
      <ShowAnswer answerId={selectedAnswerId} open={!!selectedAnswerId} handleClose={() => setSelectedAnswerId(null)} />
      <ShowScriptContents entityName={entityName} scriptId={id} open={!!entityName} handleClose={() => setEntityName(null)} />
    </Container>
  )
}
