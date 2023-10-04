import React, { useEffect, useState } from 'react'
import {
  Button, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography
} from '@mui/material'
import PropTypes from 'prop-types'
import { patch, post, remove } from '../../../api/apis'

export default function ListQuestions ({ questions, handleQuestionClick, handleAnswerClick, fetchScript }) {
  const [questionsState, setQuestionsState] = useState([])
  const [changingAnswers, setChangingAnswers] = useState([])
  const [loadingQuestions, setLoadingQuestions] = useState([])

  useEffect(() => {
    // order questions by answer_id
    const sortedQuestions = questions.sort((a, b) => {
      if (a.answer && b.answer) {
        return a.id - b.id
      } if (a.answer) {
        return 1
      } if (b.answer) {
        return -1
      }
      return 0
    })
    setQuestionsState(sortedQuestions)
  }, [questions])

  const handleDeleteQuestion = async (e, id) => {
    e.stopPropagation()
    setLoadingQuestions([...loadingQuestions, id])
    await remove('questions', id)
    setLoadingQuestions(loadingQuestions.filter((a) => a !== id))
    fetchScript()
  }

  const toggleChangingAnswer = (e, questionId) => {
    e.stopPropagation()
    const newChangingAnswers = changingAnswers.includes(questionId) ? changingAnswers.filter((a) => a !== questionId) : [...changingAnswers, questionId]
    setChangingAnswers(newChangingAnswers)
  }

  const handleChangeAnswer = async (e, question) => {
    const newContent = e.target.value
    if (newContent === question.answer?.content) {
      toggleChangingAnswer(e, question.id)
      return
    }

    setLoadingQuestions([...loadingQuestions, question.id])

    if (question.answer) {
      await patch('answers', question.answer.id, { content: newContent })
    } else {
      // create new answer
      await post('answers', { content: newContent, question: question.id })
    }

    toggleChangingAnswer(e, question.id)
    fetchScript()
    setLoadingQuestions(loadingQuestions.filter((a) => a !== question.id))
  }

  const renderAnswer = (question) => {
    if (changingAnswers.includes(question.id)) {
      return (
        <Grid flex alignContent="center">
          <TextField onBlur={(e) => handleChangeAnswer(e, question)} multiline minRows={2} autoFocus style={{ width: '70%' }} defaultValue={question.answer ? question.answer.content : ''} />
        </Grid>
      )
    }
    return (
      <Typography color={question.answer ? 'black' : 'firebrick'} onClick={(e) => toggleChangingAnswer(e, question.id)}>{question.answer ? question.answer.content : '--no-answer--'}</Typography>
    )
  }

  return (
    <TableContainer>
      <Table sx={{ width: 'fit-content' }} aria-label="simple table">
        <caption style={{ captionSide: 'top' }}>Scripts</caption>
        <TableHead>
          <TableRow>
            <TableCell>Question</TableCell>
            <TableCell>Actions</TableCell>
            <TableCell>Answer</TableCell>
            <TableCell>Answer Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {questionsState.map((question) => (
            <TableRow
              hover
              key={question.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell onClick={() => handleQuestionClick(question.id)}>{question.content}</TableCell>
              <TableCell>
                <Button variant="contained" color="error" size="small" style={{ margin: 5 }} disabled={loadingQuestions.includes(question.id)} onClick={(e) => handleDeleteQuestion(e, question.id)}>Delete</Button>
              </TableCell>
              <TableCell>
                {renderAnswer(question)}
              </TableCell>
              <TableCell>
                <Button
                  variant="contained"
                  color="warning"
                  size="small"
                  style={{ margin: 5, fontSize: 8 }}
                  disabled={loadingQuestions.includes(question.id)}
                  onClick={() => handleAnswerClick(question.answer?.id)}
                >
                  See Variations
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}

ListQuestions.propTypes = {
  questions: PropTypes.array.isRequired,
  handleAnswerClick: PropTypes.func.isRequired,
  handleQuestionClick: PropTypes.func.isRequired,
  fetchScript: PropTypes.func.isRequired
}
