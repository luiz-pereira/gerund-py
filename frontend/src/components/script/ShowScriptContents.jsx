import React, { useEffect, useState } from 'react'
import { Button, Dialog, DialogContent, DialogTitle, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material'
import PropTypes from 'prop-types'
import { get, post } from '../../api/apis'

export default function ShowScriptContents ({ entityName, scriptId, open, handleClose }) {
  const [entity, setEntity] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchEntities = async () => {
    const response = await get(`scripts/${scriptId}/${entityName}`)
    debugger
    setEntity(response)
  }

  useEffect(() => {
    if (scriptId && entityName) {
      fetchEntities()
    }
  }, [scriptId, entityName])

  const handleGenerate = async () => {
    debugger
    setLoading(true)
    const response = await post(`scripts/${scriptId}/generate_${entityName}`)
    setEntity(response)
    setLoading(false)
  }

  return (
    <Dialog onClose={handleClose} fullWidth open={open}>
      <DialogTitle>
        Script Id: {scriptId}
      </DialogTitle>
      <Button variant="outlined" disabled={loading} onClick={handleGenerate}>{`Generate ${entityName}`}</Button>
      <DialogContent>
        <Typography variant="h6">{entityName}</Typography>
      </DialogContent>
      <TableContainer>
        <Table sx={{ width: 'fit-content' }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Id</TableCell>
              <TableCell>Content</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {entity.outgoing_messages?.map((inc) => (
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

ShowScriptContents.propTypes = {
  scriptId: PropTypes.number,
  entityName: PropTypes.string.isRequired,
  open: PropTypes.bool,
  handleClose: PropTypes.func.isRequired
}
