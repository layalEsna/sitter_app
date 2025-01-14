import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

function Sitters() {
    
    const [sitters, setSitters] = useState([])

    useEffect(() => {
        fetch('http://127.0.0.1:5000/sitters')
            .then(res => {
                if (!res.ok) {
                    throw new Error('Failed to fetch sitters.')
                }
                return res.json()
            })
            .then(data => setSitters(data))
        .catch(e => console.error(e))
    }, [])

    return (
        <div>
            <h1>Pet Sitters</h1>
            <ul>
                {sitters.map(sitter => (
                    <li key={sitter.id}>
                        <button>Appointment with: {sitter.name}</button>
                        <p>Address: {sitter.location}</p>
                        <p>Price: {sitter.price}</p>
                        
                </li>

            ))}
            </ul>
        </div>
    )

}

export default Sitters