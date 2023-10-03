import React, { useEffect, useState } from 'react'
import { Button, Dialog, DialogContent, DialogTitle, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material'
import PropTypes from 'prop-types'
import { get, post } from '../../../api/apis'

export default function ShowQuestion ({ questionId, open, handleClose }) {
  const [question, setQuestion] = useState([])
  const fetchQuestion = async () => {
    const questionResponse = await get(`questions/${questionId}`)
    setQuestion(questionResponse)
  }

  useEffect(() => {
    if (questionId) {
      fetchQuestion()
    }
  }, [questionId])

  const handleGenerateVariations = async () => {
    const questionResponse = await post(`questions/${questionId}/generate_variations`)
    setQuestion(questionResponse)
  }

  return (
    <Dialog onClose={handleClose} fullWidth open={open}>
      <DialogTitle>
        Id:
        {' '}
        {question.id}
      </DialogTitle>
      <Button variant="outlined" onClick={handleGenerateVariations}>Generate Variations</Button>
      <DialogContent>
        <Typography variant="h6">Question</Typography>
        <Typography>{question.content}</Typography>
      </DialogContent>
      <TableContainer>
        <Table sx={{ width: 'fit-content' }} aria-label="simple table">
          <caption style={{ captionSide: 'top' }}>Scripts</caption>
          <TableHead>
            <TableRow>
              <TableCell>Id</TableCell>
              <TableCell>Variation</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {question.incoming_embeddings?.map((inc) => (
              <TableRow
                hover
                key={inc.id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell>{inc.id}</TableCell>
                <TableCell>{inc.content}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Dialog>
  )
}

ShowQuestion.propTypes = {
  questionId: PropTypes.number,
  open: PropTypes.bool,
  handleClose: PropTypes.func.isRequired
}
