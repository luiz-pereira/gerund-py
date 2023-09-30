import React, { useEffect, useState } from 'react'
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from '@mui/material'
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';
import PropTypes from 'prop-types'
import { patch, post, remove } from '../../../api/apis'



export default function ListQuestions({ questions, handleQuestionClick }) {
  const [questionsState, setQuestionsState] = useState([])
  const [changingAnswers, setChangingAnswers] = useState([])

  useEffect(() => {
    setQuestionsState(questions)
  }, [questions])

  const handleDeleteQuestion = (e, id) => {
    e.stopPropagation()
    remove("questions", id)
    setQuestionsState(questionsState.filter((q) => q.id !== id))
  }

  const toggleChangingAnswer = (e, questionId) => {
    e.stopPropagation()
    const newChangingAnswers = changingAnswers.includes(questionId) ? changingAnswers.filter((a) => a !== questionId) : [...changingAnswers, questionId]
    setChangingAnswers(newChangingAnswers)
  }

  const handleChangeAnswer = (e, answer, newContent) => {
    toggleChangingAnswer(e, answer.question)
    e.stopPropagation()
    if (answer.id) {
      patch("answers", answer.id, {content: newContent})
    } else {
      // create new answer
      post("answers", answer.id, {content: newContent, questionId: answer.question})
    }
  }

  const renderAnswer = (question) => {
    if (changingAnswers.includes(question.id)) {

      return <TextField onBlur={(e) => handleChangeAnswer(e, question.answer, e.target.value)} defaultValue={question.answer ? question.answer.content : ''} focused/>
    } else {
      return (<Typography color={question.answer ? 'black' : 'firebrick'} onClick={(e) => toggleChangingAnswer(e, question.id)}>{question.answer ? question.answer.content : ''}</Typography>)
    }
  }

  return (
    <TableContainer>
      <Table sx={{ width: 'fit-content' }} aria-label="simple table">
        <caption style={{captionSide: "top"}}>Scripts</caption>
        <TableHead>
          <TableRow>
            <TableCell>Question</TableCell>
            <TableCell>Answerable?</TableCell>
            <TableCell>Actions</TableCell>
            <TableCell>Answer</TableCell>
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
              <TableCell>{question.answerable ? <CheckIcon/> : <ClearIcon />}</TableCell>
              <TableCell>
                <Button variant="contained" color="error" size="small" style={{margin: 5}} onClick={(e) => handleDeleteQuestion(e, question.id)}>Delete</Button>
              </TableCell>
              <TableCell align="right">
                {renderAnswer(question)}
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
  handleQuestionClick: PropTypes.func.isRequired
}