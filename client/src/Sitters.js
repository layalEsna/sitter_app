import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

function Sitter() {
    
    const [sitters, setSitters] = useState([])

    useEffect(() => {
        fetch('http://localhost:5000/sitters')
            .then(res => {
                if (!res.ok) {
                    throw new Error('Failed to fetch sitters.')
                }
                return res.json()
            })
            .then(data => setSitters(data))
        .catch(e => console.error(e))
    }, [])

}

export default Sitter