import React, { useEffect, useState } from 'react'
import { Button, Dialog, DialogContent, DialogTitle, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material'
import PropTypes from 'prop-types'
import { get, post } from '../../../api/apis'

export default function ShowAnswer ({ answerId, open, handleClose }) {
  const [answer, setAnswer] = useState([])
  const fetchAnswer = async () => {
    const answerResponse = await get(`answers/${answerId}`)
    setAnswer(answerResponse)
  }

  useEffect(() => {
    if (answerId) {
      fetchAnswer()
    }
  }, [answerId])

  const handleGenerateVariations = async () => {
    const answerResponse = await post(`answers/${answerId}/generate_variations`)
    setAnswer(answerResponse)
  }

  return (
    <Dialog onClose={handleClose} fullWidth open={open}>
      <DialogTitle>
        Id:
        {' '}
        {answer.id}
      </DialogTitle>
      <Button variant="outlined" onClick={handleGenerateVariations}>Generate Variations</Button>
      <DialogContent>
        <Typography variant="h6">Answer</Typography>
        <Typography>{answer.content}</Typography>
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
            {answer.outgoing_messages?.map((inc) => (
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

ShowAnswer.propTypes = {
  answerId: PropTypes.number,
  open: PropTypes.bool,
  handleClose: PropTypes.func.isRequired
}
