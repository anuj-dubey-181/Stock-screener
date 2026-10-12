import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

const API_URL = 'https://stock-screener-backend-okep.onrender.com'


export function AuthProvider({ children }) {

  const [token, setToken] = useState(
    localStorage.getItem('access_token')
  )


  async function login(email, password) {

    const response = await fetch(
      `${API_URL}/auth/login`,
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          email: email,
          password: password
        })
      }
    )


    const data = await response
      .json()
      .catch(() => null)


    if (!response.ok) {

      throw new Error(
        data?.detail ||
        `Login failed (${response.status})`
      )

    }


    if (!data?.access_token) {

      throw new Error(
        'Login response does not contain an access token.'
      )

    }


    // Store JWT
    localStorage.setItem(
      'access_token',
      data.access_token
    )


    // Update React state
    setToken(data.access_token)


    return data
  }


  function logout() {

    localStorage.removeItem(
      'access_token'
    )

    setToken(null)
  }


  return (

    <AuthContext.Provider
      value={{
        token,
        isAuthenticated: !!token,
        login,
        logout
      }}
    >

      {children}

    </AuthContext.Provider>

  )
}


export function useAuth() {

  const context = useContext(
    AuthContext
  )


  if (!context) {

    throw new Error(
      'useAuth must be used inside AuthProvider'
    )

  }


  return context
}
