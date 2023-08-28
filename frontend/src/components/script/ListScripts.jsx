import React, { useEffect, useState } from 'react'
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'
import { get } from '../../api/apis'
import { useNavigate } from "react-router-dom";


export default function ListScripts() {
  const navigate = useNavigate();
  const [scripts, setScripts] = useState([])

  const fetchScripts = async () => {
    const scriptsResponse = await get('scripts')
    setScripts(scriptsResponse)
  }

  useEffect(() => {
    fetchScripts()
  }, [])

  return (
    <TableContainer>
      <Table sx={{ width: 200 }} aria-label="simple table">
        <caption style={{captionSide: "top"}}>Scripts</caption>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell align="right">id</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {scripts.map((row) => (
            <TableRow
              hover
              key={row.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              onClick={() => navigate(`/scripts/${row.id}`)}
            >
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell align="right">{row.id}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}
