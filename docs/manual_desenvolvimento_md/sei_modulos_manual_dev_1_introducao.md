# 1. Introdução

O Sistema Eletrônico de Informações (SEI) possui uma API (`Application Programming Interface`) que permite o desenvolvimento de módulos. Por meio dessa API os módulos podem:

- **adicionar botões e ícones específicos** em diversas funcionalidades do core do SEI, como na tela de Controle de Processos e na visualização da árvore de documentos dos processos;

- **incluir itens de menu** nas telas de usuários internos, de usuários externos e de pesquisa de publicações;

- **interceptar eventos** do sistema para tratamento específico, como no momento da assinatura de documentos, do envio de processos e do cancelamento de documentos;

- **realizar operações** no sistema, como geração de processos, lançamento de andamentos no histórico e inclusão de documentos.

Na seção **InfraPHP** consta uma descrição resumida do framework PHP do sistema. Algumas classes do framework são descritas ao longo deste documento, pois a interação com elas será obrigatória devido a questões de segurança e integração com o sistema.

Para evitar conflitos com outros módulos recomendamos que ao nomear os artefatos, como classes, recursos e tabelas, seja utilizado o prefixo md seguido de até três letras que identifique o módulo (`md_jul`, `md_pet`, `md_lit`, etc).

- Este documento contém também seções descrevendo o **Padrão de Modelagem de Dados** e o **Padrão de Codificação PHP** utilizados no SEI.
