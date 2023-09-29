import React, { useEffect, useState } from 'react'
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';
import PropTypes from 'prop-types'
import { remove } from '../../../api/apis'



export default function ListQuestions({ questions, handleRowClick }) {
  const [questionsState, setQuestionsState] = useState([])

  useEffect(() => {
    setQuestionsState(questions)
  }, [questions])

  const handleDeleteQuestion = (e, id) => {
    e.stopPropagation()
    remove("questions", id)
    setQuestionsState(questionsState.filter((q) => q.id !== id))
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
              onClick={() => handleRowClick(question.id)}
            >
              <TableCell>{question.content}</TableCell>
              <TableCell>{question.answerable ? <CheckIcon/> : <ClearIcon />}</TableCell>
              <TableCell>
                <Button variant="contained" color="error" size="small" style={{margin: 5}} onClick={(e) => handleDeleteQuestion(e, question.id)}>Delete</Button>
              </TableCell>
              <TableCell align="right" style={{color: question.answer ? 'black' : 'firebrick'}}>{question.answer ? question.answer.content : '-- no answer --'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}

ListQuestions.propTypes = {
  questions: PropTypes.array.isRequired,
  handleRowClick: PropTypes.func.isRequired
}