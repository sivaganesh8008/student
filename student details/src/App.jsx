
import { useState } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState('')
  const [pin, setPin] = useState('')
  const [students, setStudents] = useState([])

  const addStudent = () => {
    if (name === '' || pin === '') {
      alert('Please enter name and PIN')
      return
    }

    const newStudent = {
      name: name,
      pin: pin
    }

    setStudents([...students, newStudent])

    // Clear input fields
    setName('')
    setPin('')
  }

  return (
    <>
      <h1>Student Details</h1>

      <input
        type="text"
        placeholder="Enter Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <input
        type="text"
        placeholder="Enter PIN Number"
        value={pin}
        onChange={(e) => setPin(e.target.value)}
      />

      <button onClick={addStudent}>Add</button>

      <br />
      <br />

      <table border="1">
        <thead>
          <tr>
            <th>S.No</th>
            <th>Name</th>
            <th>PIN Number</th>
          </tr>
        </thead>

        <tbody>
          {students.map((student, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{student.name}</td>
              <td>{student.pin}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

export default App
