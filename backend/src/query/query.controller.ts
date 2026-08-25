import { Body, Controller, Post } from '@nestjs/common';
import { QueryResult, QueryService } from './query.service';

class AskDto {
  pregunta: string;
}

@Controller('query')
export class QueryController {
  constructor(private readonly queryService: QueryService) {}

  @Post()
  ask(@Body() body: AskDto): Promise<QueryResult> {
    return this.queryService.ask(body.pregunta);
  }
}
