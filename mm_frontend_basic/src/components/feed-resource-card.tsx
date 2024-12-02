'use client'

import Link from 'next/link'
import { useParams } from 'next/navigation'

import { cn, formatDate } from '@/lib/utils'

import { useTagParams } from '@/hooks/use-tag-params'

import type { FeedTagResource } from '@/types/resourceType'
import { Tables } from '@/types/database.types'

interface Props {
  resource: Tables<'resources'>
}

export function ResourceCard({ resource }: Props) {
  const params = useParams<{ id: string }>()
  const tag = useTagParams()

  return (
    <article>
      <Link
        className={cn(
          'inline-flex size-full flex-col space-y-1 rounded-md p-2 text-sm text-muted-foreground transition-colors hover:bg-accent focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring xl:p-3',
          params.id === resource.id && 'bg-accent',
        )}
        href={
          tag
            ? `/resources/${resource.id}?${new URLSearchParams({ tag })}`
            : `/resources/${resource.id}`
        }
        prefetch
      >
        <div className="flex justify-between space-x-2 text-xs">
          <span>{new URL(resource.url).hostname}</span>
          <span>{formatDate(resource.created_at)}</span>
        </div>
        <div>
          <h2 className="line-clamp-2 text-foreground">{resource.title}</h2>
          <p className="line-clamp-1">{resource.description}</p>
        </div>
      </Link>
    </article>
  )
}
