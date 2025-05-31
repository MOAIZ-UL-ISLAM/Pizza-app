"use client"

import { useForm } from "react-hook-form"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import { verifyOTP } from "@/services/auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"
import { VerifyOTP } from "@/types/auth"

const verifyOTPSchema = z.object({
  email: z.string().email("Invalid email address"),
  otp_code: z.string().length(6, "OTP must be 6 digits"),
})

type VerifyOTPFormData = z.infer<typeof verifyOTPSchema>

export default function VerifyOTPForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<VerifyOTPFormData>({
    resolver: zodResolver(verifyOTPSchema),
  })

  const verifyOTPMutation = useMutation({
    mutationFn: verifyOTP,
    onSuccess: (data) => {
      console.log(data.detail)
    },
    onError: (error) => {
      console.error("OTP verification failed:", error)
    },
  })

  const onSubmit = (data: VerifyOTPFormData) => {
    verifyOTPMutation.mutate(data)
  }

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Verify OTP</CardTitle>
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
          <Button type="submit" className="w-full" disabled={verifyOTPMutation.isPending}>
            {verifyOTPMutation.isPending ? "Verifying..." : "Verify OTP"}
          </Button>
        </form>
        <div className="mt-4 text-center">
          <Link href="/forgot-password" className="text-primary hover:underline">
            Request New OTP
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}