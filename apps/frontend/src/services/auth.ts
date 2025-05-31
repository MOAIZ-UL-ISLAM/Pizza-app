import api from "./api"
import { LoginCredentials, RegisterData, ForgotPasswordData, VerifyOTPData, ResetPasswordData } from "@/types/auth"

export const login = async (credentials: LoginCredentials) => {
    const response = await api.post("/jwt/create/", credentials)
    return response.data
}

export const register = async (data: RegisterData) => {
    const response = await api.post("/users/", data)
    return response.data
}

export const requestPassword = async (data: ForgotPasswordData) => {
    const response = await api.post("/password/reset/", data)
    return response.data
}

export const verifyOTP = async (data: VerifyOTPData) => {
    const response = await api.post("/password/reset/verify-otp/", data)
    return response.data
}

export const resetPassword = async (data: ResetPasswordData) => {
    const response = await api.post("/password/reset/confirm/", data)
    return response.data
}

export const getUser = async () => {
    const response = await api.get("/me/")
    return response.data
}