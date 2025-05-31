"use client"

import { useForm } from "react-hook-form"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import { resetPassword } from "@/services/auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"
import { ResetPasswordData } from "@/types/auth"

const resetPasswordSchema = z.object({
    email: z.string().email("Invalid email address"),
    otp_code: z.string().length(6, "OTP must be 6 digits"),
    new_password: z.string().regex(/^\d{8}$/, "Password must be exactly 8 digits"),
    confirm_password: z.string().regex(/^\d{8}$/, "Password must be exactly 8 digits"),
}).refine((data) => data.new_password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
})

type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>

export default function ResetPasswordForm() {
    const { register, handleSubmit, formState: { errors } } = useForm<ResetPasswordFormData>({
        resolver: zodResolver(resetPasswordSchema),
    })

    const resetPasswordMutation = useMutation({
        mutationFn: resetPassword,
        onSuccess: (data) => {
            console.log(data.detail)
        },
        onError: (error) => {
            console.error("Password reset failed:", error)
        },
    })

    const onSubmit = (data: ResetPasswordFormData) => {
        resetPasswordMutation.mutate(data)
    }

    return (
        <Card className="w-full max-w-md">
            <CardHeader>
                <CardTitle>Reset Password</CardTitle>
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
                            placeholder="OTP Code"
                            {...register("otp_code")}
                            className={errors.otp_code ? "border-destructive" : ""}
                        />
                        {errors.otp_code && (
                            <p className="text-destructive text-sm mt-1">{errors.otp_code.message}</p>
                        )}
                    </div>
                    <div>
                        <Input
                            type="password"
                            placeholder="New Password"
                            {...register("new_password")}
                            className={errors.new_password ? "border-destructive" : ""}
                        />
                        {errors.new_password && (
                            <p className="text-destructive text-sm mt-1">{errors.new_password.message}</p>
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
                    <Button type="submit" className="w-full" disabled={resetPasswordMutation.isPending}>
                        {resetPasswordMutation.isPending ? "Resetting..." : "Reset Password"}
                    </Button>
                </form>
                <div className="mt-4 text-center">
                    <Link href="/login" className="text-primary hover:underline">
                        Back to Login
                    </Link>
                </div>
            </CardContent>
        </Card>
    )
}