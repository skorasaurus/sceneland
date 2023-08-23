import Head from 'next/head'
import { allShows } from 'src/data/allShows'
import { useState } from 'react'
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuCheckboxItem } from 'src/components/dropdown'

export const getStaticProps = async () => {
  return { 
    props: {
      shows: allShows
    }
  }
}

// UI to filter results by venue
export function VenueFilter({ venues, selectedVenues, onVenueToggle }) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger className='group dropdown-button w-auto px-4 py-2 font-medium rounded-full text-base bg-zinc-950 hover:bg-zinc-800 transition text-zinc-50 dark:bg-zinc-50 dark:text-zinc-800 border border-zinc-400 dark:border-white dark:hover:bg-zinc-200 focus:outline-none focus:ring focus:ring-indigo-500/50'>
        Select your fav Cleveland venues{' '}
        <span className='inline-block text-zinc-400 transition group-hover:translate-y-0.5 transform -rotate-90'>
          &lt;
        </span>
      </DropdownMenuTrigger>
        {venues.map(venue => (
      <DropdownMenuContent className='dark:bg-zinc-50 min-w-[200px] md:min-w-[360px] rounded-xl shadow-lg shadow-black/5 flex flex-col bg-zinc-900'>
          <DropdownMenuCheckboxItem
            key={venue.replace(/[^\w]+/g, '-').toLowerCase()}
            checked={selectedVenues.includes(venue)}
            onCheckedChange={() => onVenueToggle(venue)}
          >
            {venue}
          </DropdownMenuCheckboxItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export default function Home() {
  // Create an array of all unique venues
  const allVenues = Array.from(new Set(allShows.map(show => show.venue)));

  // Initialize state for selected venues
  const [selectedVenues, setSelectedVenues] = useState(allVenues);

  // Handle venue toggling by changing state
  const handleVenueToggle = venue => {
    // If the `selectedVenues` array already includes the venue, remove it
    if (selectedVenues.includes(venue)) {
      setSelectedVenues(selectedVenues.filter(v => v !== venue));
    } else {
      // If the venue is not in the `selectedVenues` array, add it  
      setSelectedVenues([...selectedVenues, venue]);
    }
  };
  
  // Filter shows by selected venues
  const filteredShows = allShows.filter(show => selectedVenues.includes(show.venue));
  
  // Sort filtered shows chronologically by show date
  const sortedFilteredShows = filteredShows.sort((a, b) => new Date(a.date) - new Date(b.date));

  return (
    <>
      <Head>
        <title>216.show: Music in Cleveland 🤘</title>
        <meta name='description' content='Concerts coming up at your fav local venues like the Beachland, Agora, Mahall’s, and more' />
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <link rel='icon' href='/favicon.png' />
      </Head>
      
      <header className='text-center mx-auto items-center flex max-md:flex-col md:justify-center md:gap-x-4 p-4 lg:p-8 gap-2 text-sm sticky top-0 shadow-xl dark:shadow-black/25 shadow-black/[0.03] border-b border-b-black/10 dark:border-b-white/5 bg-zinc-50 dark:bg-black/50 backdrop-blur'>
        <h1 className='text-xl font-mono md:tracking-tight md:font-semibold md:uppercase md:text-2xl text-zinc-800 dark:text-zinc-200'>
          216.show
        </h1>
        <VenueFilter
          venues={allVenues} // pass the array of all unique venues names as a prop
          selectedVenues={selectedVenues} // pass the array of selected (checked) venues as a prop
          onVenueToggle={handleVenueToggle} // pass the function to handle toggling as a prop
        />
      </header>
      
        {sortedFilteredShows.map((show, i) => (
          show.artist && (
            <a
              key={i}
              href={show.link}
            >
                {JSON.stringify(show.artist).replace(/\[|\]|\"/g,'').replace(/\,/g, ', ')}
                {' '}
              </h2>
                {new Date(show.date).toLocaleDateString('en-US', {weekday: 'short', year: 'numeric', month: 'long', day: 'numeric'})}
              </time>
            </a>
          )
        ))}
      <main className='grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-8 lg:grid-cols-3 xl:grid-cols-4 container mx-auto p-4 lg:p-8'>
              <a key={i} href={show.link} className='group flex flex-col h-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded leading-snug p-4 gap-y-2 shadow-sm dark:shadow-md transition hover:dark:border-zinc-700 hover:border-zinc-300 hover:shadow-black/10  focus:outline-none focus:ring focus:ring-indigo-500/25'>
                {show.sold_out && <span className='self-start uppercase border transition rounded-full [text-shadow:_0_1px_0_rgb(0_0_0_/_40%)] px-2.5 py-1 text-xs font-semibold tracking-wide whitespace-nowrap dark:text-red-500 text-white border-red-700 dark:border-red-900/75 group-hover:dark:border-red-900 dark:bg-red-950 bg-red-600'>Sold out</span>}
                <h2 className='font-semibold dark:font-medium text-zinc-800 dark:text-zinc-300'>
                <span className='font-mono text-sm'>{show.venue}</span>
                <time className='flex-1 flex items-end mt-3 text-zinc-800 dark:text-zinc-300' dateTime={new Date(show.date)}>
      </main>
      
        <p>
          All data is pulled from the venues’ individual websites and aggregated here. No ownership of information is claimed nor implied.
        </p>
      <footer className='container mx-auto p-4 lg:p-8 text-sm flex flex-col gap-2 text-center'>
        <p>
          Support your scene and take care of each other.
        </p>
      </footer>
    </>
  )
}
