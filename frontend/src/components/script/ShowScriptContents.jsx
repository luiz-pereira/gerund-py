import React, { useEffect, useState } from 'react'
import { Button, Dialog, DialogContent, DialogTitle, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material'
import PropTypes from 'prop-types'
import { get, post } from '../../api/apis'

export default function ShowScriptContents ({ entityName, scriptId, open, handleClose }) {
  const [entities, setEntities] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchEntities = async () => {
    const response = await get(`scripts/${scriptId}/${entityName}`)
    setEntities(response)
  }

  useEffect(() => {
    if (scriptId && entityName) {
      fetchEntities()
    }
  }, [scriptId, entityName])

  const handleGenerate = async () => {
    setLoading(true)
    await post(`scripts/${scriptId}/generate_${entityName}`)
    fetchEntities()
    setLoading(false)
  }

  return (
    <Dialog onClose={handleClose} fullWidth open={open} >
      <DialogTitle>
        Script Id: {scriptId}
      </DialogTitle>
      <DialogContent style={{ textAlign: 'center', overflowY: 'unset' }}>
        <Button variant="outlined" style={{ width: 'fit-content' }} disabled={loading} onClick={handleGenerate}>{`Generate ${entityName}`}</Button>
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
            {entities.map((entity) => (
              <TableRow
                hover
                key={entity.id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell>{entity.id}</TableCell>
                <TableCell>{entity.content}</TableCell>
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
