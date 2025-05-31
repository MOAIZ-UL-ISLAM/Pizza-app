"use client"

import { useForm } from "react-hook-form"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import { useAppDispatch } from "@/store/hooks"
import { setCredentials } from "@/store/slices/authSlice"
import { register } from "@/services/auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"
import { RegisterData } from "@/types/auth"

const registerSchema = z.object({
    email: z.string().email("Invalid email address"),
    username: z.string().min(3, "Username must be at least 3 characters"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirm_password: z.string().min(8, "Password must be at least 8 characters"),
}).refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
})

type RegisterFormData = z.infer<typeof registerSchema>

export default function RegisterForm() {
    const dispatch = useAppDispatch()
    const { register, handleSubmit, formState: { errors } } = useForm<RegisterFormData>({
        resolver: zodResolver(registerSchema),
    })

    const registerMutation = useMutation({
        mutationFn: register,
        onSuccess: (data) => {
            dispatch(setCredentials({ user: data.user, token: data.access }))
        },
        onError: (error) => {
            console.error("Registration failed:", error)
        },
    })

    const onSubmit = (data: RegisterFormData) => {
        registerMutation.mutate(data)
    }

    return (
        <Card className="w-full max-w-md">
            <CardHeader>
                <CardTitle>Register</CardTitle>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div>
                        <Input
                            type="email"
                            placeholder="Email"
                            {...register("email")}
                            className={errors.email ? "border-destructive" : ""}
                        />
                        {errors.email && (
                            <p className="text-destructive text-sm mt-1">{errors.email.message}</p>
                        )}
                    </div>
                    <div>
                        <Input
                            type="text"
                            placeholder="Username"
                            {...register("username")}
                            className={errors.username ? "border-destructive" : ""}
                        />
                        {errors.username && (
                            <p className="text-destructive text-sm mt-1">{errors.username.message}</p>
                        )}
                    </div>
                    <div>
                        <Input
                            type="password"
                            placeholder="Password"
                            {...register("password")}
                            className={errors.password ? "border-destructive" : ""}
                        />
                        {errors.password && (
                            <p className="text-destructive text-sm mt-1">{errors.password.message}</p>
                        )}
                    </div>
                    <div>
                        <Input
                            type="password"
                            placeholder="Confirm Password"
                            {...register("confirm_password")}
                            className={errors.confirm_password ? "border-destructive" : ""}
                        />
                        {errors.confirm_password && (
                            <p className="text-destructive text-sm mt-1">{errors.confirm_password.message}</p>
                        )}
                    </div>
                    <Button type="submit" className="w-full" disabled={registerMutation.isPending}>
                        {registerMutation.isPending ? "Registering..." : "Register"}
                    </Button>
                </form>
                <div className="mt-4 text-center">
                    <p>
                        Already have an account?{" "}
                        <Link href="/login" className="text-primary hover:underline">
                            Login
                        </Link>
                    </p>
                </div>
            </CardContent>
        </Card>
    )
}