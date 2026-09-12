import { useState, useEffect } from 'react'
import './App.css'

function App() {

  const [name, setName] = useState('')
  const [pin, setPin] = useState('')
  const [students, setStudents] = useState([])

  const [editingId, setEditingId] = useState(null)


  // ==================================================
  // GET ALL STUDENTS
  // ==================================================

  const getStudents = async () => {

    try {

      const response = await fetch(
        'http://127.0.0.1:5000/students'
      )

      const data = await response.json()

      setStudents(data)

    } catch (error) {

      console.error('Error:', error)

      alert('Unable to connect to server')

    }
  }


  // ==================================================
  // LOAD STUDENTS WHEN PAGE OPENS
  // ==================================================

  useEffect(() => {

    getStudents()

  }, [])


  // ==================================================
  // ADD STUDENT
  // ==================================================

  const addStudent = async () => {

    if (name.trim() === '' || pin.trim() === '') {

      alert('Please enter name and PIN')

      return
    }

    try {

      const response = await fetch(
        'http://127.0.0.1:5000/students',
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            name: name,
            pin: pin
          })
        }
      )

      const data = await response.json()

      if (response.ok) {

        alert(data.message)

        // Clear inputs
        setName('')
        setPin('')

        // Get updated students
        getStudents()

      } else {

        alert(data.message)

      }

    } catch (error) {

      console.error('Error:', error)

      alert('Unable to connect to server')

    }
  }


  // ==================================================
  // DELETE STUDENT
  // ==================================================

  const deleteStudent = async (id) => {

    const confirmDelete = window.confirm(
      'Are you sure you want to delete this student?'
    )

    if (!confirmDelete) {
      return
    }

    try {

      const response = await fetch(
        `http://127.0.0.1:5000/students/${id}`,
        {
          method: 'DELETE'
        }
      )

      const data = await response.json()

      if (response.ok) {

        alert(data.message)

        getStudents()

      } else {

        alert(data.message)

      }

    } catch (error) {

      console.error('Error:', error)

      alert('Unable to connect to server')

    }
  }


  // ==================================================
  // START EDIT
  // ==================================================

  const startEdit = (student) => {

    setEditingId(student.id)

    setName(student.name)

    setPin(student.pin)
  }


  // ==================================================
  // UPDATE STUDENT
  // ==================================================

  const updateStudent = async () => {

    if (name.trim() === '' || pin.trim() === '') {

      alert('Please enter name and PIN')

      return
    }

    try {

      const response = await fetch(
        `http://127.0.0.1:5000/students/${editingId}`,
        {
          method: 'PUT',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            name: name,
            pin: pin
          })
        }
      )

      const data = await response.json()

      if (response.ok) {

        alert(data.message)

        // Clear
        setName('')
        setPin('')
        setEditingId(null)

        // Refresh table
        getStudents()

      } else {

        alert(data.message)

      }

    } catch (error) {

      console.error('Error:', error)

      alert('Unable to connect to server')

    }
  }


  // ==================================================
  // CANCEL EDIT
  // ==================================================

  const cancelEdit = () => {

    setEditingId(null)

    setName('')

    setPin('')
  }


  // ==================================================
  // UI
  // ==================================================

  return (
    <div>

      <h1>Student Details</h1>


      {/* INPUTS */}

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


      {/* BUTTONS */}

      {editingId === null ? (

        <button onClick={addStudent}>
          Add Student
        </button>

      ) : (

        <>
          <button onClick={updateStudent}>
            Update Student
          </button>

          <button onClick={cancelEdit}>
            Cancel
          </button>
        </>

      )}


      <br />
      <br />


      {/* STUDENT TABLE */}

      <h2>All Students</h2>


      <table border="1">

        <thead>

          <tr>

            <th>S.No</th>

            <th>Name</th>

            <th>PIN Number</th>

            <th>Actions</th>

          </tr>

        </thead>


        <tbody>

          {students.length === 0 ? (

            <tr>

              <td colSpan="4">
                No students found
              </td>

            </tr>

          ) : (

            students.map((student, index) => (

              <tr key={student.id}>

                <td>
                  {index + 1}
                </td>

                <td>
                  {student.name}
                </td>

                <td>
                  {student.pin}
                </td>

                <td>

                  <button
                    onClick={() => startEdit(student)}
                  >
                    Edit
                  </button>


                  <button
                    onClick={() => deleteStudent(student.id)}
                  >
                    Delete
                  </button>

                </td>

              </tr>

            ))

          )}

        </tbody>

      </table>

    </div>
  )
}

export default App