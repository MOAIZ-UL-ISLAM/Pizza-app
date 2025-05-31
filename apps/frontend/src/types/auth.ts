export interface LoginCredentials {
    email: string
    password: string
}

export interface RegisterData {
    email: string
    username: string
    password: string
    confirm_password: string
}

export interface ForgotPasswordData {
    email: string
}

export interface VerifyOTPData {
    email: string
    otp_code: string
}

export interface ResetPasswordData {
    email: string
    otp_code: string
    new_password: string
    confirm_password: string
}

export interface User {
    id: string
    email: string
    username: string
    date_joined: string
}