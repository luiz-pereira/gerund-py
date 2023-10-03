import React, { useEffect, useState } from 'react'
import { Button, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from '@mui/material'
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';
import PropTypes from 'prop-types'
import { patch, post, remove } from '../../../api/apis'



export default function ListQuestions({ questions, handleQuestionClick, fetchScript }) {
  const [questionsState, setQuestionsState] = useState([])
  const [changingAnswers, setChangingAnswers] = useState([])

  useEffect(() => {
    setQuestionsState(questions)
  }, [questions])

  const handleDeleteQuestion = (e, id) => {
    e.stopPropagation()
    remove("questions", id)
    fetchScript()
  }

  const toggleChangingAnswer = (e, questionId) => {
    e.stopPropagation()
    const newChangingAnswers = changingAnswers.includes(questionId) ? changingAnswers.filter((a) => a !== questionId) : [...changingAnswers, questionId]
    setChangingAnswers(newChangingAnswers)
  }

  const handleChangeAnswer = (e, question) => {
    e.stopPropagation()

    const newContent = e.target.value
    toggleChangingAnswer(e, question.id)

    if (newContent === question.answer?.content) {
      return
    }

    if (question.answer) {
      patch("answers", question.answer.id, {content: newContent})
    } else {
      // create new answer
      post("answers", {content: newContent, question: question.id})
    }
    fetchScript()
  }

  const renderAnswer = (question) => {
    if (changingAnswers.includes(question.id)) {

      return (
        <Grid flex={true} alignContent={"center"}>
          <TextField onBlur={(e) => handleChangeAnswer(e, question)} multiline minRows={2} autoFocus style={{width: "70%"}} defaultValue={question.answer ? question.answer.content : ''}/>
        </Grid>
      )
    } else {
      return (<Typography color={question.answer ? 'black' : 'firebrick'} onClick={(e) => toggleChangingAnswer(e, question.id)}>{question.answer ? question.answer.content : '--no-answer--'}</Typography>)
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
              <TableCell>
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
  handleQuestionClick: PropTypes.func.isRequired,
  fetchScript: PropTypes.func.isRequired
}
