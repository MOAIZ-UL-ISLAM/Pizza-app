'use client'
import { useAppDispatch, useAppSelector } from "@/store/hooks"
import { clearCredentials } from "@/store/slices/authSlice"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function Navbar() {
  const dispatch = useAppDispatch()
  const { isAuthenticated } = useAppSelector((state) => state.auth)

  const handleLogout = () => {
    dispatch(clearCredentials())
  }

  return (
    <nav className="bg-primary text-primary-foreground p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold">
          Auth App
        </Link>
        <div className="space-x-4">
          {isAuthenticated ? (
            <>
              <Link href="/dashboard">
                <Button variant="ghost">Dashboard</Button>
              </Link>
              <Button variant="ghost" onClick={handleLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link href="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link href="/register">
                <Button variant="ghost">Register</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}