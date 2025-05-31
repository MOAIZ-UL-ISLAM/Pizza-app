import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { User } from "@/types/auth"

interface AuthState {
    user: User | null
    token: string | null
    isAuthenticated: boolean
}

const initialState: AuthState = {
    user: null,
    token: null,
    isAuthenticated: false,
}

const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        setCredentials: (
            state,
            action: PayloadAction<{ user: User; token: string }>
        ) => {
            state.user = action.payload.user
            state.token = action.payload.token
            state.isAuthenticated = true
            localStorage.setItem("token", action.payload.token)
        },
        clearCredentials: (state) => {
            state.user = null
            state.token = null
            state.isAuthenticated = false
            localStorage.removeItem("token")
        },
    },
})

export const { setCredentials, clearCredentials } = authSlice.actions
export default authSlice.reducer