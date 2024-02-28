"use client";
import {
  BellIcon,
  CogIcon,
  HomeIcon
} from "@/components/Icons";
import { Inter } from "next/font/google";
import Image from "next/image";
import { usePathname } from "next/navigation";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex h-screen bg-gray-100">
          <aside className="w-64 px-8 py-4 bg-white">
            <div className="flex items-center justify-center pb-6 mb-6 border-b border-gray-200 mt-3">
              <span className="ml-3 text-lg font-semibold text-blue-600">
                Drive, Live, Die
              </span>
            </div>
            <nav className="mb-10">
              <a
                className={`flex items-center px-4 py-2 mt-5 text-gray-700 rounded-md ${!pathname.includes("products") && !pathname.includes("recipes") ? "bg-gray-100" : "hover:text-gray-700 hover:bg-gray-50"}`}
                href="/"
              >
                <HomeIcon className="h-6 w-6" />
                <span className="mx-4 font-medium">Dashboard</span>
              </a>
              {/* <a
                className={`flex items-center px-4 py-2 mt-5 text-gray-700 rounded-md ${pathname.includes("products") ? "bg-gray-100" : "hover:text-gray-700 hover:bg-gray-50"}`}
                href="/products"
              >
                <UsersIcon className="h-6 w-6" />
                <span className="mx-4 font-medium">Produkty</span>
              </a>
              <a
                className={`flex items-center px-4 py-2 mt-5 text-gray-700 rounded-md ${pathname.includes("recipes") ? "bg-gray-100" : "hover:text-gray-700 hover:bg-gray-50"}`}
                href="/recipes"
              >
                <BriefcaseIcon className="h-6 w-6" />
                <span className="mx-4 font-medium">Przepisy</span>
              </a> */}
            </nav>
            <div className="absolute bottom-0 my-10">
              <a
                className="flex items-center px-4 py-2 mt-5 text-gray-600 hover:text-gray-700 hover:bg-gray-50 rounded-md"
                href="#"
              >
                <CogIcon className="h-6 w-6" />
                <span className="mx-4 font-medium">Ustawienia</span>
              </a>
            </div>
          </aside>
          <div className="flex-1 px-4 py-8">
            <div className="flex justify-between">
              <div className="flex space-x-4">
                {/* <SearchIcon className="w-5 h-5 text-gray-500" />
            <input
              className="w-full px-2 py-2 leading-tight text-gray-700 bg-gray-200 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
              placeholder="Search..."
              type="text"
            /> */}
              </div>
              <div className="flex items-center space-x-4">
                <BellIcon className="w-5 h-5 text-gray-600" />
                <div className="relative">
                  <button className="relative z-10 block overflow-hidden rounded-full focus:outline-none">
                    <Image
                      src="/avatar1.png"
                      alt="Avatar"
                      width={32}
                      height={32}
                      className="object-cover rounded-full"
                    />
                  </button>
                </div>
              </div>
            </div>
            <div className="flex justify-center mt-8">
              <div className="w-full h-full p-6 bg-white rounded-lg shadow-lg">
                <div className="rounded-lg h-[calc(100vh_-_250px)] text-black">
                  {children}
                </div>
              </div>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}
