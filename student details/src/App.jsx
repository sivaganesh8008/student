
import { useState } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState('')
  const [pin, setPin] = useState('')
  const [students, setStudents] = useState([])

  const addStudent = async () => {
    if (name === '' || pin === '') {
      alert('Please enter name and PIN')
      return
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/students', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          pin: pin
        })
      })

      const data = await response.json()

      if (response.ok) {
        alert('Student added successfully')

        // Add student to table
        const newStudent = {
          name: name,
          pin: pin
        }

        setStudents([...students, newStudent])

        // Clear inputs
        setName('')
        setPin('')
      } else {
        alert(data.message)
      }

    } catch (error) {
      console.error(error)
      alert('Cannot connect to Python server')
    }
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

      <button onClick={addStudent}>
        Add
      </button>

      <br />
      <br />

      <table>
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
