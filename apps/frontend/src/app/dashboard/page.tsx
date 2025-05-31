"use client"

import { useQuery } from "@tanstack/react-query"
import { useAppSelector } from "@/store/hooks"
import { getUser } from "@/services/auth"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useRouter } from "next/navigation"
import { useEffect } from "react"

export default function DashboardPage() {
    const { isAuthenticated } = useAppSelector((state) => state.auth)
    const router = useRouter()

    useEffect(() => {
        if (!isAuthenticated) {
            router.push("/login")
        }
    }, [isAuthenticated, router])

    const { data: user, isLoading } = useQuery({
        queryKey: ["user"],
        queryFn: getUser,
        enabled: isAuthenticated,
    })

    if (!isAuthenticated) return null

    if (isLoading) return <div>Loading...</div>

    return (
        <div className="container mx-auto py-8">
            <Card className="w-full max-w-md mx-auto">
                <CardHeader>
                    <CardTitle>Welcome, {user?.username}!</CardTitle>
                </CardHeader>
                <CardContent>
                    <p>Email: {user?.email}</p>
                    <p>Joined: {new Date(user?.date_joined).toLocaleDateString()}</p>
                </CardContent>
            </Card>
        </div>
    )
}