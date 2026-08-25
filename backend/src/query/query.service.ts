import { HttpService } from '@nestjs/axios';
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom } from 'rxjs';

export interface Fuente {
  chunk: string;
  distancia: number;
}

export interface QueryResult {
  respuesta: string;
  fuentes: Fuente[];
}

@Injectable()
export class QueryService {
  constructor(
    private readonly httpService: HttpService,
    private readonly configService: ConfigService,
  ) {}

  async ask(pregunta: string): Promise<QueryResult> {
    const ragApiUrl = this.configService.get<string>(
      'RAG_API_URL',
      'http://localhost:8000',
    );

    const response = await firstValueFrom(
      this.httpService.post<QueryResult>(`${ragApiUrl}/query`, { pregunta }),
    );

    return response.data;
  }
}
