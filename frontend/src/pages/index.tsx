import Head from 'next/head'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <>
      <Head>
        <title>EU AI Act Compliance Bot</title>
        <meta name="description" content="Automated regulatory assessment for AI systems under EU AI Act" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={`min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 ${inter.className}`}>
        <div className="container mx-auto px-4 py-16">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              EU AI Act 
              <span className="text-blue-600"> Compliance Bot</span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Automated regulatory assessment for AI systems under the EU AI Act. 
              Get instant compliance analysis, risk categorization, and actionable recommendations.
            </p>
            
            <div className="mb-12">
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-8 rounded-lg text-lg transition-colors mr-4">
                Start Assessment
              </button>
              <button className="border border-gray-300 hover:border-gray-400 text-gray-700 font-semibold py-4 px-8 rounded-lg text-lg transition-colors">
                Learn More
              </button>
            </div>
            
            <div className="grid md:grid-cols-4 gap-8 text-center">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-3xl font-bold text-red-500 mb-2">Unacceptable</div>
                <div className="text-gray-600">Prohibited AI practices</div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-3xl font-bold text-orange-500 mb-2">High Risk</div>
                <div className="text-gray-600">Strict requirements</div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-3xl font-bold text-yellow-500 mb-2">Limited</div>
                <div className="text-gray-600">Transparency obligations</div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-3xl font-bold text-green-500 mb-2">Minimal</div>
                <div className="text-gray-600">No specific obligations</div>
              </div>
            </div>
            
            <div className="mt-16 text-center">
              <div className="text-sm text-gray-500">
                🚀 Market Opportunity: EU AI Act enforcement starts 2026
              </div>
              <div className="text-sm text-gray-500 mt-1">
                Help your organization ensure compliance with automated assessment
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}