import React from 'react'
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';
import PropTypes from 'prop-types'



export default function ListQuestions({ questions, handleRowClick }) {
  return (
    <TableContainer>
      <Table sx={{ width: 'fit-content' }} aria-label="simple table">
        <caption style={{captionSide: "top"}}>Scripts</caption>
        <TableHead>
          <TableRow>
            <TableCell>Question</TableCell>
            <TableCell>Answerable?</TableCell>
            <TableCell>Answer</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {questions.map((question) => (
            <TableRow
              hover
              key={question.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              onClick={() => handleRowClick(question.id)}
            >
              <TableCell>{question.content}</TableCell>
              <TableCell>{question.answerable ? <CheckIcon/> : <ClearIcon />}</TableCell>
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